from schemas import PutPiece, FieldPost
from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from functions import field

router = APIRouter(
    prefix = "/field",
    tags = ["field"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_field(db:Session=Depends(get_db)):
    return field.read(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def post_field(db:Session=Depends(get_db)):
    return field.create(db)

@router.put("/", status_code=status.HTTP_200_OK)
def update_field(field_update:FieldPost, db:Session=Depends(get_db)):
    return field.update(field_update, db)

@router.put("/piece/")
def put_piece_to_field(put_piece:PutPiece, db:Session=Depends(get_db)):
    return field.put_piece(put_piece, db)
