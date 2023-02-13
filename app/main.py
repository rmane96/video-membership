from fastapi import FastAPI, Request, Form
from app.config import get_settings
from cassandra.cqlengine.management import sync_table
from app.users.models import User
from app.db import get_session
import pathlib
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



BASE_DIR = pathlib.Path(__file__).resolve().parent 
TEMPLATE_DIR = BASE_DIR / "templates" 


app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.on_event("startup")
def on_startup():
    get_session()
    sync_table(User)
    
settings = get_settings()
        


@app.get('/login',response_class=HTMLResponse)
def login_post(request: Request, email:str=Form(...),password:str=Form(...)):
    context = {
        "request": request
    }
    return templates.TemplateResponse("auth/login.html",context)


@app.post('/login',response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("auth/login.html",context)


@app.post('/signup',response_class=HTMLResponse)
def signup_post(
    request: Request, 
    email:str=Form(...),
    password:str=Form(...),
    password_confirm:str=Form(...)
    ):
    context = {
        "request": request
    }
    return templates.TemplateResponse("auth/signup.html",context)


@app.get('/signup',response_class=HTMLResponse)
def signup_get(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("auth/signup.html",context)

