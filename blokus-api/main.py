from fastapi import FastAPI, Depends, Query, status, Response, HTTPException, Request
from fastapi.responses import HTMLResponse
from schemas import PiecePost, FieldPost, PutPiece, PlayerPost
from models import PieceBase, PieceFR, Field, Player, PlayerPieces
# from . import models
from database import engine, sessionLocal, Base, get_db
from sqlalchemy.orm import Session
from jinja2 import Template, Environment, FileSystemLoader
# from .piece import rotate
# import json
# from rotate import rotate
import itertools
import requests
# pieces_fr = rotate.pieces_fr
# p_fr_base = {}

from routes import piece, field

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))

URL = "http://localhost:8000/"
app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(piece.router)
app.include_router(field.router)

@app.get("/")
def get_rendered_field_by_jinja2(request:Request,db:Session=Depends(get_db)):
    url = URL + "field/"
    txt = requests.get(url).json()
    tmpl = env.get_template('render.j2')
    c = tmpl.render(field=txt)
    return HTMLResponse(content=c)


@app.post("/player/")
def create_player(player_post:PlayerPost, db:Session=Depends(get_db)):
    new_player = Player(
        name = player_post.name,
        turn = player_post.turn,
        is_current_player = player_post.is_current,
    )
    db.add(new_player)
    db.commit()


@app.post("/player/pieces/")
def give_all_pieces_to_player(db:Session=Depends(get_db)):
    players = db.query(Player).all()
    pieces = db.query(PieceBase).all()
    for player, piece in itertools.product(players, pieces):
        e = PlayerPieces(
            player_id = player.id,
            piecebase_id = piece.id
        )
        db.add(e)
    db.commit()
    db.refresh(e)
    return "done"