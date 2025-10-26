import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from main import run_all_agents

app = FastAPI(title="Agentic Authoring Assistant")
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
templates_dir = os.path.join(current_dir, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")


# HTML templates folder
templates = Jinja2Templates(directory=templates_dir)

# Home page with form
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

# Handle form submission
@app.post("/generate", response_class=HTMLResponse)
def generate(request: Request, text: str = Form(...)):
    result = run_all_agents(text)
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
