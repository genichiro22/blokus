import models
from schemas import PutPiece, FieldPost
from sqlalchemy.orm import Session
# from fastapi import status
from functions import validation

def read(id:int, db:Session):
    game = db.query(models.Game).filter(models.Game.id==id).first()
    # print(field)
    return game

def create(db:Session):
    game = models.Game()
    db.add(game)
    # print(game.id)
    db.flush()
    # print(game.id)
    for x in range(20):
        for y in range(20):
            plot = models.GameField(
                game_id=game.id,
                x=x,
                y=y
            )
            db.add(plot)
    db.commit()
    game.id # これがないと何故かflush前のgameがreturnされてしまう
    return game