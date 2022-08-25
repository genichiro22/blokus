from schemas import PutPiece, FieldPost
from fastapi import APIRouter, Depends, status, Path
from database import get_db
from sqlalchemy.orm import Session
from functions import field
import models
import oauth2

router = APIRouter(
    prefix = "/{game_id}/field",
    tags = ["gamefield"]
)

def query_game_by_id(game_id:int, db:Session=Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id==game_id).first()
    return game

@router.get("/", status_code=status.HTTP_200_OK)
# def get_field(game:models.Game=Depends(oauth2.get_current_game), db:Session=Depends(get_db)):
def get_field(game_id:int, db:Session=Depends(get_db)):
    game = query_game_by_id(game_id, db)
    return field.read(game, db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def post_empty_field(game_id:int, db:Session=Depends(get_db)):
    game = query_game_by_id(game_id, db)
    return field.create(game, db)

@router.put("/", status_code=status.HTTP_200_OK)
def update_field(game_id:int, field_update:FieldPost, db:Session=Depends(get_db)):
    game = query_game_by_id(game_id, db)
    return field.update(game, field_update, db)

@router.put("/piece/")
def put_piece_to_field(game_id:int, put_piece:PutPiece, db:Session=Depends(get_db)):
    game = query_game_by_id(game_id, db)
    return field.put_piece(game, put_piece, db)
