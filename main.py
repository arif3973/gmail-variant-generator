from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "variants": None})

def generate_variants(email):
    try:
        local_part, domain = email.split("@")
    except ValueError:
        return []

    variants = set()

    def backtrack(s, pos):
        if pos == len(local_part):
            variants.add(s)
            return
        backtrack(s + local_part[pos].lower(), pos + 1)
        backtrack(s + local_part[pos].upper(), pos + 1)

    backtrack("", 0)
    return [v + "@" + domain for v in variants]

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, email: str = Form(...)):
    variants = generate_variants(email)
    return templates.TemplateResponse("index.html", {"request": request, "variants": variants})
