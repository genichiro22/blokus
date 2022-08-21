from schemas import PlayerPost
from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from functions import player

router = APIRouter(
    prefix = "/player",
    tags = ["player"]
)

@router.post("/")
def create_player(player_post:PlayerPost, db:Session=Depends(get_db)):
    return player.create(player_post, db)


@router.post("/pieces/")
def give_all_pieces_to_player(db:Session=Depends(get_db)):
    return player.give_all_pieces(db)