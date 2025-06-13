from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Capitalization variant generator
def generate_capitalization_variants(email: str):
    if not email or "@" not in email:
        return []

    local_part, domain = email.split("@", 1)

    if not local_part or not domain:
        return []

    variants = set()

    def backtrack(index, current):
        if index == len(local_part):
            variants.add(current + "@" + domain)
            return
        backtrack(index + 1, current + local_part[index].lower())
        backtrack(index + 1, current + local_part[index].upper())

    backtrack(0, "")
    return sorted(variants)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "variants": [], "too_many": False})

@app.post("/", response_class=HTMLResponse)
async def generate(
    request: Request,
    email: str = Form(...),
    limit: int = Form(...)
):
    all_variants = generate_capitalization_variants(email.strip())
    limited_variants = all_variants[:limit]
    too_many = len(all_variants) > limit

    return templates.TemplateResponse("index.html", {
        "request": request,
        "variants": limited_variants,
        "too_many": too_many,
        "email": email
    })
