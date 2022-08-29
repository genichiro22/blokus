from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from token___ import verify_token
from env.settings import TEMPLATE_ENV

# def get(current_user):
def get(request:Request, db:Session):
    tmpl = TEMPLATE_ENV.get_template('render.j2')
    token = request.cookies.get("access_token").removeprefix("Bearer ")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = verify_token(token, credentials_exception, db=db)
    c = tmpl.render(player_name=user.name)
    return HTMLResponse(content=c)