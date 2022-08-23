import models
from schemas import NewUser
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def create(new_user:NewUser, db:Session):
    user = models.User(
        name = new_user.name,
        raw_pwd = new_user.pwd,
    )
    db.add(user)
    db.commit()
    return user

def show(id:int, db:Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    return user
"""
def give_all_pieces(db:Session):
    players = db.query(models.Player).all()
    pieces = db.query(models.PieceBase).all()
    for player, piece in itertools.product(players, pieces):
        e = models.PlayerPieces(
            player_id = player.id,
            piecebase_id = piece.id
        )
        db.add(e)
    db.commit()
    db.refresh(e)
    return "done"
"""