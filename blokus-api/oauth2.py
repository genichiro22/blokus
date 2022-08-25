from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from token___ import verify_token
from sqlalchemy.orm import Session
from database import get_db
import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(token: str=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    result = verify_token(token, credentials_exception, db)
    return result

def get_current_game(token: str=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    game = db.query(models.Game).join(models.GamePlayer).filter(models.GamePlayer.user_id==user.id).first()
    # print(game)
    # return game.field
    return game