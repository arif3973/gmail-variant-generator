from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "variants": None, "too_many": False})

def generate_variants(email, max_limit=1500):
    try:
        local_part, domain = email.split("@")
    except ValueError:
        return []

    variants = set()

    def backtrack(s, pos):
        if len(variants) >= max_limit:
            return
        if pos == len(local_part):
            variants.add(s)
            return
        backtrack(s + local_part[pos].lower(), pos + 1)
        backtrack(s + local_part[pos].upper(), pos + 1)

    backtrack("", 0)
    return [v + "@" + domain for v in variants]

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, email: str = Form(...), limit: int = Form(...)):
    max_limit = min(limit, 1500)
    variants = generate_variants(email, max_limit=max_limit)
    too_many = len(variants) >= max_limit
    return templates.TemplateResponse("index.html", {
        "request": request,
        "variants": variants,
        "too_many": too_many
    })
