from schemas import PutPiece, FieldPost
from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from jinja2 import Template, Environment, FileSystemLoader
from fastapi.responses import HTMLResponse
from functions import frontend
import oauth2
import models

router = APIRouter(
    tags = ["frontend"]
)

@router.get("/")
def get_rendered_field(current_player: models.Player=Depends(oauth2.get_current_user)):
    return frontend.get(current_player)