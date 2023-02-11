from fastapi import FastAPI
from app.config import get_settings
from cassandra.cqlengine.management import sync_table
from app.users.models import User
from app.db import get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    get_session()
    sync_table(User)
    
        

settings = get_settings()

@app.get('/')
def root():
    return {
        "data":"Hello World"
    }


# @app.get('/users'):

