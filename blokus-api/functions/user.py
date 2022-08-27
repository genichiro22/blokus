import models
from schemas import NewUser
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def create(new_user:NewUser, db:Session):
    u = db.query(models.User).filter(models.User.name==new_user.name).all()
    if u:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User name {new_user.name} already exists"
        )
    user = models.User(
        name = new_user.name,
        raw_pwd = new_user.pwd,
    )
    db.add(user)
    db.commit()
    user.id
    return user

def show(id:int, db:Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    return user
