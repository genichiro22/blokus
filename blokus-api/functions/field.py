import models
from schemas import PutPiece, FieldPost
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Request
from functions import validation
from oauth2 import get_current_user_from_cookie

# def read(game:models.Game, db:Session):
def read(game:models.Game):
    # field = db.query(models.GameField).filter(models.GameField.game_id==game.id).all()
    return game.field

def create(game:models.Game, db:Session):
    for x in range(20):
        for y in range(20):
            plot = models.GameField(game_id=game.id, x=x, y=y)
            db.add(plot)
    db.commit()
    db.refresh(plot)
    return

def update(game:models.Game, field_update:FieldPost, db:Session):
    player = field_update.player
    for c in field_update.coordinates:
        current_field = db.query(models.GameField).filter(
            models.GameField.x == c.x,
            models.GameField.y == c.y,
            models.GameField.game_id==game.id
        )
        field = {
            "x": c.x,
            "y": c.y,
            "player": player
        }
        current_field.update(field)
    db.commit()
    return "updated"

def put_piece(game:models.Game, put_piece:PutPiece, request:Request, db:Session):
    token = request.cookies.get("access_token")
    user = get_current_user_from_cookie(token, db)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "You are not assigned to this game"
        )
    # print(user.name)
    p = db.query(models.GamePlayer).join(models.Game).filter(
        models.Game.id == game.id,
        models.GamePlayer.user_id == user.id,
    ).first()
    if not p:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "You are not assigned to this game"
        )
    player = p.player
    piece = db.query(models.PieceFR).filter(models.PieceFR.piecebase_id==put_piece.piece_id, models.PieceFR.fliprot_id==put_piece.fr_id).all()
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    v = validation.validation(game, put_piece, player, db)
    v.whole()
    for c in coordinates:
        current_field = db.query(models.GameField).filter(
            models.GameField.x == c["x"],
            models.GameField.y == c["y"],
            models.GameField.game_id==game.id
        )
        current_field.update(
            {"player": player}
        )
    q = db.query(models.Game).filter(models.Game.id==game.id)
    turn = q.first().turn
    q.update({"turn": turn+1})
    db.query(models.PlayerPieces).filter(
        models.PlayerPieces.player==player,
        models.PlayerPieces.piecebase_id==put_piece.piece_id
    ).delete()
    db.commit()
