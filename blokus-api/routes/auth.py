from os import access
from urllib.request import Request
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
import models
import token___
from schemas import Login
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Auth']
)

@router.post('/login')
def login(
    response: Response,
    request: OAuth2PasswordRequestForm=Depends(),
    db: Session=Depends(get_db)
):
    user = db.query(models.User).filter(models.User.name==request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid Credentials'
        )
    # if not Hash.verify(request.password, user.password):
    if not request.password == user.raw_pwd:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'Incorrect Password'
        )
    access_token = token___.create_access_token(
        data={"sub": user.name, "id": user.id}
    )
    response.set_cookie(
        key="access_token", value = f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout")
def logout(response:Response):
    response.delete_cookie(
        key="access_token"
    )
    return True