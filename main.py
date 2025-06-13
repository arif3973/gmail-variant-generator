from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from itertools import product
from pathlib import Path
from starlette.templating import Jinja2Templates

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR))

def generate_variants(email: str, limit: int = 500):
    if not email.endswith("@gmail.com"):
        return []

    local, domain = email.split("@")
    if not local.isalpha():
        return []

    variants = set()
    local = local.lower()
    positions = list(product(*[(c.lower(), c.upper()) for c in local]))
    
    for p in positions[:limit]:
        variants.add("".join(p) + "@gmail.com")

    return sorted(variants)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def generate(request: Request, email: str = Form(...), limit: int = Form(...)):
    variants = generate_variants(email, limit)
    return HTMLResponse(
        content="<ul>" + "".join(
            f'<li><span>{v}</span> <button class="copy-btn">Copy</button></li>'
            for v in variants
        ) + "</ul>" if variants else "<p>No variants found.</p>",
        status_code=200
    )
