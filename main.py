from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

MAX_LIMIT = 1500  # সর্বোচ্চ সীমা

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "variants": None,
        "too_many": False
    })

def generate_variants(email: str, limit: int):
    try:
        local_part, domain = email.split("@")
    except ValueError:
        return [], False

    variants = set()
    too_many = False

    def backtrack(s, pos):
        nonlocal too_many
        if len(variants) >= limit:
            too_many = len(variants) < (2 ** len(local_part))  # সীমা পেরিয়ে গেছে কিনা
            return
        if pos == len(local_part):
            variants.add(s)
            return
        backtrack(s + local_part[pos].lower(), pos + 1)
        backtrack(s + local_part[pos].upper(), pos + 1)

    backtrack("", 0)
    variants_list = [v + "@" + domain for v in variants]
    return variants_list, too_many

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, email: str = Form(...), limit: int = Form(...)):
    # সীমা যেন ১৫০০ এর বেশি না হয়
    final_limit = min(limit, MAX_LIMIT)
    variants, too_many = generate_variants(email, final_limit)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "variants": variants,
        "too_many": too_many
    })
