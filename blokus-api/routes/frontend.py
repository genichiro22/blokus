from schemas import PutPiece, FieldPost
from fastapi import APIRouter, Depends, status, Request, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from jinja2 import Template, Environment, FileSystemLoader
from fastapi.responses import HTMLResponse
from functions import frontend
import oauth2
import models

from token___ import verify_token

router = APIRouter(
    tags = ["frontend"]
)

@router.get("/")
# def get_rendered_field(current_user: models.User=Depends(oauth2.get_current_user)):
def get_rendered_field(request:Request, db:Session=Depends(get_db)):
    t = request.cookies.get("access_token")
    print(t)
    t2 = t.removeprefix("Bearer ")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    t3 = verify_token(t2, credentials_exception, db=db)
    print(t3.name)
    return frontend.get(t3.name)