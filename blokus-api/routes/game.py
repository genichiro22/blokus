from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from functions import game
from schemas import UserToPlayer
from . import field

router = APIRouter(
    prefix = "/game",
    tags = ["game"]
)

router.include_router(field.router)

@router.get("/{id}/", status_code=status.HTTP_200_OK)
def read_game(id:int, db:Session=Depends(get_db)):
    return game.read(id, db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_game(db:Session=Depends(get_db)):
    return game.create(db)

@router.post("/{id}/", status_code=status.HTTP_201_CREATED)
def assign_user(id:int, user_to_player:UserToPlayer, db:Session=Depends(get_db)):
    return game.add_player(id, user_to_player, db)
