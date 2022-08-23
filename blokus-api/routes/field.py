from schemas import PutPiece, FieldPost
from fastapi import APIRouter, Depends, status, Path
from database import get_db
from sqlalchemy.orm import Session
from functions import field

router = APIRouter(
    prefix = "/{game_id}/field",
    tags = ["gamefield"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_field(game_id:int, db:Session=Depends(get_db)):
    return field.read(game_id, db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def post_field(game_id:int, db:Session=Depends(get_db)):
    return field.create(game_id, db)

@router.put("/", status_code=status.HTTP_200_OK)
def update_field(game_id:int, field_update:FieldPost, db:Session=Depends(get_db)):
    return field.update(game_id, field_update, db)

@router.put("/piece/")
def put_piece_to_field(game_id:int, put_piece:PutPiece, db:Session=Depends(get_db)):
    return field.put_piece(game_id, put_piece, db)
