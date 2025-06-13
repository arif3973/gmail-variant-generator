from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itertools import product
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def generate_variants(email: str, limit: int = 1500):
    if "@gmail.com" not in email:
        return []

    local_part, domain = email.lower().split("@")
    positions = list(range(len(local_part)))
    variations = []

    for combo in product(*[(c.lower(), c.upper()) for c in local_part]):
        variant = "".join(combo)
        if variant not in variations:
            variations.append(f"{variant}@{domain}")
        if len(variations) >= limit:
            break

    return variations


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def generate(request: Request, email: str = Form(...), limit: int = Form(...)):
    variants = generate_variants(email.strip(), limit)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "email": email,
        "limit": limit,
        "variants": variants
    })
