import models
from schemas import PutPiece, FieldPost
from sqlalchemy.orm import Session
# from fastapi import status
from functions import validation

def read(game:models.Game, db:Session):
    field = db.query(models.GameField).filter(models.GameField.game_id==game.id).all()
    return field

def create(game_id:int, db:Session):
    for x in range(20):
        for y in range(20):
            plot = models.GameField(game_id=game_id, x=x, y=y)
            db.add(plot)
    db.commit()
    db.refresh(plot)
    return

def update(field_update:FieldPost, db:Session):
    player = field_update.player
    for c in field_update.coordinates:
        current_field = db.query(models.GameField).filter(models.GameField.x == c.x, models.GameField.y == c.y)
        field = {
            "x": c.x,
            "y": c.y,
            "value": player
        }
        current_field.update(field)
    db.commit()
    return "updated"

def put_piece(game_id:int, put_piece:PutPiece, db:Session):
    # print(put_piece)
    # print(1)
    piece = db.query(models.PieceFR).filter(models.PieceFR.piecebase_id==put_piece.piece_id, models.PieceFR.fliprot_id==put_piece.fr_id).all()
    # print(piece)
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    # print(coordinates)
    validation.whole(game_id, put_piece, db)
    field_post = FieldPost(
        player=put_piece.player,
        coordinates=coordinates
    )
    update(field_post, db)
    query = db.query(models.Game).filter(models.Game.current_player == put_piece.player)
    player = query.first()
    update_player = {"turn": player.turn+1, "is_current_player": False}
    query.update(update_player)
    db.query(models.User).filter(models.User.id == put_piece.player%4+1).update({"is_current_player": True})
    db.query(models.PlayerPieces).filter(
        models.PlayerPieces.player==put_piece.player,
        models.PlayerPieces.piecebase_id==put_piece.piece_id
    ).delete()
    # new_turn = {"current_player_id": put_piece.player%4+1}
    # db.query(TurnControl).update(new_turn)
    db.commit()



