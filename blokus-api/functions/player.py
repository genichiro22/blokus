import models
from schemas import PlayerPost
from sqlalchemy.orm import Session
import itertools

def create(player_post:PlayerPost, db:Session):
    new_player = models.Player(
        name = player_post.name,
        turn = 0,
        raw_pwd = player_post.pwd,
        is_current_player = player_post.is_first,
    )
    db.add(new_player)
    db.commit()

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