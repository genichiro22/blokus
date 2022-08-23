from fastapi import HTTPException, status
import models
from sqlalchemy.orm import Session
from schemas import UserToPlayer

def read(id:int, db:Session):
    game = db.query(models.Game).filter(models.Game.id==id).first()
    return game

def create(db:Session):
    game = models.Game()
    db.add(game)
    db.flush()
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

def add_player(game_id:int, user_to_player:UserToPlayer, db:Session):
    user_id = user_to_player.user_id
    player = user_to_player.player
    query = db.query(models.GamePlayer).filter(models.GamePlayer.game_id == game_id)
    check1 = query.filter(models.GamePlayer.user_id == user_id).first()
    if check1:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"User {user_id} is already assigned to game {game_id}"
        )
    check2 = query.filter(models.GamePlayer.player == player).first()
    if check2:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"Another user {check2.user_id} is already assigned to player {player} of game {game_id}"
        )
    new_player = models.GamePlayer(
        user_id = user_id,
        game_id = game_id,
        player = player
    )
    db.add(new_player)
    pieces = db.query(models.PieceBase).all()
    for piece in pieces:
        e = models.PlayerPieces(
            game_id=game_id,
            player=player,
            piecebase_id=piece.id
        )
        db.add(e)
    db.commit()
    return new_player
