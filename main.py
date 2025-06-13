from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from io import StringIO
import itertools

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def generate_variants(email, limit=500):
    try:
        local, domain = email.split('@')
        if domain.lower() != 'gmail.com':
            return ["Only @gmail.com supported."]
    except Exception:
        return []

    variants = set()
    for mask in itertools.product(*[(c.lower(), c.upper()) if c.isalpha() else (c,) for c in local]):
        variant = ''.join(mask) + "@" + domain
        variants.add(variant)
        if len(variants) >= limit:
            break
    return list(variants)

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "variants": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, email: str = Form(...), limit: int = Form(100)):
    limit = min(limit, 1500)  # max limit 1500
    variants = generate_variants(email, limit)
    return templates.TemplateResponse("index.html", {"request": request, "variants": variants, "email": email, "limit": limit})

@app.post("/download")
async def download_variants(email: str = Form(...), limit: int = Form(100)):
    limit = min(limit, 1500)
    variants = generate_variants(email, limit)
    if not variants:
        variants = ["No variants found."]
    text = "\n".join(variants)
    stream = StringIO(text)
    headers = {
        'Content-Disposition': f'attachment; filename="{email}_variants.txt"'
    }
    return StreamingResponse(stream, media_type='text/plain', headers=headers)
