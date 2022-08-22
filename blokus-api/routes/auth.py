from fastapi import APIRouter, Depends, status, HTTPException
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
    request: OAuth2PasswordRequestForm=Depends(),
    db: Session=Depends(get_db)
):
    player = db.query(models.Player).filter(models.Player.name==request.username).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid Credentials'
        )
    # if not Hash.verify(request.password, user.password):
    if not request.password == player.raw_pwd:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'Incorrect Password'
        )
    access_token = token___.create_access_token(
        data={"sub": player.name, "id": player.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}