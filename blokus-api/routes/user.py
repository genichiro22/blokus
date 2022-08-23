from schemas import NewUser
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from functions import user

router = APIRouter(
    prefix = "/user",
    tags = ["user"]
)

@router.post("/")
def create_user(new_user:NewUser, db:Session=Depends(get_db)):
    return user.create(new_user, db)

@router.get("/{id}/")
def read_user(id:int, db:Session=Depends(get_db)):
    return user.show(id,db)