from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Capitalization variant generator
def generate_capitalization_variants(email: str):
    try:
        local_part, domain = email.split("@")
    except ValueError:
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
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def generate(
    request: Request,
    email: str = Form(...),
    limit: int = Form(...)
):
    all_variants = generate_capitalization_variants(email)
    limited_variants = all_variants[:limit]
    too_many = len(all_variants) > limit

    return templates.TemplateResponse("index.html", {
        "request": request,
        "variants": limited_variants,
        "too_many": too_many,
        "email": email
    })
