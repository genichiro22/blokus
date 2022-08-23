from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from functions import game

router = APIRouter(
    prefix = "/game",
    tags = ["game"]
)

@router.get("/{id}/", status_code=status.HTTP_200_OK)
def read_game(id:int, db:Session=Depends(get_db)):
    return game.read(id, db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_game(db:Session=Depends(get_db)):
    return game.create(db)