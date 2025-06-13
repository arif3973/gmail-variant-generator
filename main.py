from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

MAX_LIMIT = 1500

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
        return []

    variants = set()

    def backtrack(s: str, pos: int):
        if len(variants) >= limit:
            return
        if pos == len(local_part):
            variants.add(s + "@" + domain)
            return
        backtrack(s + local_part[pos].lower(), pos + 1)
        backtrack(s + local_part[pos].upper(), pos + 1)

    backtrack("", 0)
    return list(variants)

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, email: str = Form(...), limit: int = Form(...)):
    final_limit = min(limit, MAX_LIMIT)
    variants = generate_variants(email, final_limit)
    too_many = limit > MAX_LIMIT
    return templates.TemplateResponse("index.html", {
        "request": request,
        "variants": variants,
        "too_many": too_many
    })
