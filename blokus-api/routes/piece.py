from fastapi import APIRouter, Depends, status, HTTPException
from schemas import PiecePost
# import models
from database import get_db
from sqlalchemy.orm import Session
from functions import piece

router = APIRouter(
    prefix = "/pieces",
    tags = ["pieces"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def post(piece_:PiecePost, db:Session=Depends(get_db),):
    return piece.create_piece(piece_, db)

@router.get("/{piece_name}/", status_code=status.HTTP_200_OK)
def get(piece_name:str, db:Session=Depends(get_db)):
    return piece.read_piece(piece_name, db)

@router.post("/all/")
def post_fr_all(db:Session=Depends(get_db)):
    return piece.fr_all(db)

@router.get("/{piece_name}/{id}", status_code=status.HTTP_200_OK)
def post_fr(piece_name:str, id:int, db:Session=Depends(get_db)):
    return piece.fr(piece_name, id, db)
