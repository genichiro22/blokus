from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import PieceName
from .models import PieceName, Piece
from . import models
from .database import engine, sessionLocal, Base
from sqlalchemy.orm import Session
# from .piece import rotate
import json
# pieces_fr = rotate.pieces_fr
# p_fr_base = {}

app = FastAPI()
Base.metadata.create_all(engine)

# @app.get("/")
# def index():
#     return json.dumps(p_fr_base)
@app.get("/")
def index():
    return ""

'''
@app.get("/{piece_name}/", status_code=status.HTTP_200_OK)
def fr(piece_name:str, response:Response):
    if piece_name not in p_fr_base.keys():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Piece name of {piece_name} is not available"
        )
    return json.dumps(p_fr_base[piece_name])

@app.get("/{piece_name}/{id}", status_code=status.HTTP_200_OK)
def fr(piece_name:str, id:int, response:Response):
    if piece_name not in p_fr_base.keys():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Piece name of {piece_name} is not available"
        )
    if id>=len(p_fr_base[piece_name]):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Index {id} is not found in flip-rotation of the piece {piece_name}"
        )
    return json.dumps(p_fr_base[piece_name][id])
'''