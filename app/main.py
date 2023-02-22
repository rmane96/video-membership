from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from cassandra.cqlengine.management import sync_table
from pydantic.error_wrappers import ValidationError
import pathlib, json
from app.config import get_settings
from app.users.models import User
from app.db import get_session
from app.users.schemas import UserLoginSchema, UserSignupSchema
from app import utils
from app.shortcuts import render



BASE_DIR = pathlib.Path(__file__).resolve().parent 
TEMPLATE_DIR = BASE_DIR / "templates" 


app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.on_event("startup")
def on_startup():
    get_session()
    # sync_table(User)
    
settings = get_settings()
        

""" Login """

@app.get('/login',response_class=HTMLResponse)
def login_get(request: Request):
    return render(request,'auth/login.html',{})


@app.post('/login',response_class=HTMLResponse)
def login_post(request: Request):
    email:str=Form(...)
    password:str=Form(...)
    print(email,password)
    raw_data = {
        "email":email,
        "password":password
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    return render(request,"auth/login.html",{
        'data':data,
        'errors':errors,
    })


""" Signup """


@app.get('/signup',response_class=HTMLResponse)
def login_get(request: Request):
    return render(request,'auth/signup.html',{})


@app.post("/signup", response_class=HTMLResponse)
def signup_post(request: Request, 
    email: str=Form(...), 
    password: str = Form(...),
    password_confirm: str = Form(...)
    ):
    raw_data  = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    return render(request, "auth/signup.html", {
        "data":data,
        "errors":errors,
    })

