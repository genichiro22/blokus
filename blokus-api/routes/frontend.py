from schemas import PutPiece, FieldPost
from fastapi import APIRouter, Depends, status, Request, HTTPException, Response
from database import get_db
from sqlalchemy.orm import Session
from jinja2 import Template, Environment, FileSystemLoader
from fastapi.responses import HTMLResponse
from functions import frontend, game
import oauth2
import models
from env.settings import TEMPLATE_ENV

router = APIRouter(
    tags = ["frontend"],
    prefix= "/frontend"
)

@router.get("/game/")
def get_games(request:Request, db:Session=Depends(get_db)):
    games = db.query(models.Game).all()
    tmpl = TEMPLATE_ENV.get_template("games.j2")
    token = request.cookies.get("access_token")
    user = oauth2.get_current_user_from_cookie(token)
    c = tmpl.render(games=games, user=user)
    return HTMLResponse(content=c)

@router.get("/game/{id}/")
def get_rendered_field(id:int, request:Request, db:Session=Depends(get_db)):
    return frontend.get(id, request, db)

@router.get("/login/")
def login_front():
    tmpl = TEMPLATE_ENV.get_template('login.j2')
    c = tmpl.render()
    return HTMLResponse(content=c)

@router.get("/logout/")
def logout(response:Response):
    response.delete_cookie(
        key="access_token"
    )
    return True