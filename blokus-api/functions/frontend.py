from fastapi.responses import HTMLResponse
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from token___ import verify_token
import models
from env.settings import TEMPLATE_ENV

# def get(current_user):
def get(id:int, request:Request, db:Session):
    q = db.query(models.Game).filter(models.Game.id==id).all()
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Game {id} is not available"
        )
    tmpl = TEMPLATE_ENV.get_template('render.j2')
    # token = request.cookies.get("access_token").removeprefix("Bearer ")
    token = request.cookies.get("access_token")
    if not token:
        name = "Guest"
    else:
        if token[0:7] == "Bearer ":
        # print(token[0:7])
        # token.replace(token[0:7],"")
            token = token[7:len(token)]
        # print(token)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user = verify_token(token, credentials_exception, db=db)
        name = user.name
        player = db.query(models.GamePlayer).join(models.Game).filter(models.Game.id==id, models.GamePlayer.user_id==user.id).first()
        turn = None if not player else player.player
    c = tmpl.render(
        player_name = name,
        player_turn = turn,
        game_id = id
    )
    return HTMLResponse(content=c)