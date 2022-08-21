from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
# from . import models
from database import engine, Base, get_db
from sqlalchemy.orm import Session
from jinja2 import Template, Environment, FileSystemLoader
import requests
from routes import piece, field, player

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))

URL = "http://localhost:8000/"
app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(piece.router)
app.include_router(field.router)
app.include_router(player.router)

@app.get("/")
def get_rendered_field_by_jinja2(request:Request,db:Session=Depends(get_db)):
    url = URL + "field/"
    txt = requests.get(url).json()
    tmpl = env.get_template('render.j2')
    c = tmpl.render(field=txt)
    return HTMLResponse(content=c)
