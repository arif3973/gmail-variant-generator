from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def generate_variants(email: str, limit: int = 100):
    local, domain = email.split("@")
    unique_variants = set()
    max_combinations = 2 ** (len(local) - 1)
    limit = min(limit, max_combinations)
    for i in range(max_combinations):
        variant = ""
        for j in range(len(local)):
            variant += local[j]
            if j < len(local) - 1 and (i >> j) & 1:
                variant += "."
        unique_variants.add(f"{variant}@{domain}")
        if len(unique_variants) >= limit:
            break
    return list(unique_variants)

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, email: str = Form(...), limit: int = Form(...)):
    variants = generate_variants(email, limit)
    return templates.TemplateResponse("index.html", {"request": request, "variants": variants, "email": email, "limit": limit})
