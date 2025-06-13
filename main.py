from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from typing import List
from itertools import product

app = FastAPI()

def generate_case_variants(username: str, domain: str = "gmail.com", limit: int = 500) -> List[str]:
    options = [(c.lower(), c.upper()) if c.isalpha() else (c,) for c in username]
    variants = [''.join(p) + '@' + domain for p in product(*options)]
    return variants[:limit]

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Gmail Variant Generator</title>
        </head>
        <body>
            <h1>Gmail Variant Generator</h1>
            <form action="/generate" method="post">
                <label for="email">Enter Gmail:</label>
                <input type="text" name="email" required>
                <br><br>
                <label for="limit">Limit (max 500):</label>
                <input type="number" name="limit" value="500" min="1" max="500">
                <br><br>
                <input type="submit" value="Generate">
            </form>
        </body>
    </html>
    """

@app.post("/generate")
async def generate_variants(email: str = Form(...), limit: int = Form(500)):
    if '@' not in email:
        return {"error": "Invalid email format."}
    
    username, domain = email.split('@')

    if domain.lower() != "gmail.com":
        return {"error": "Only gmail.com domain is supported."}
    
    variants = generate_case_variants(username, domain, limit)
    return {
        "input": email,
        "count": len(variants),
        "variants": variants
    }
