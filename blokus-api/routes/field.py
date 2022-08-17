import models
from schemas import PutPiece, FieldPost
from fastapi import APIRouter, Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from functions import field

router = APIRouter(
    prefix = "/field",
    tags = ["field"]
)

@router.get("/")
def get_field(db:Session=Depends(get_db), status_code=status.HTTP_200_OK):
    return field.read(db, status_code)

@router.post("/")
def post_field(db:Session=Depends(get_db), status_code=status.HTTP_201_CREATED):
    return field.create(db, status_code)

@router.put("/")
def update_field(field_update:FieldPost, db:Session=Depends(get_db), status_code=status.HTTP_200_OK):
    return field.update(field_update, db, status_code)

@router.put("/piece/")
def put_piece_to_field(put_piece:PutPiece, db:Session=Depends(get_db)):
    return field.put_piece(put_piece, db)
