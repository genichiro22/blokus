from email.mime import base
from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import PiecePost
from .models import PieceBase, PieceFR
from . import models
from .database import engine, sessionLocal, Base, get_db
from sqlalchemy.orm import Session
# from .piece import rotate
import json
import numpy as np
from .rotate import rotate
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

@app.post("/", status_code=status.HTTP_201_CREATED)
def post_piece(piece:PiecePost, db:Session=Depends(get_db),):
    # print(base_shape)
    # print(piece.base_shape)
    coordinates = [{"x":c.x, "y":c.y} for c in piece.base_shape]
    # print(coordinates)
    # print(json.dumps(coordinates))
    # base_shape = piece.base_shape
    new_piece = models.PieceBase(
        name = piece.name,
        base_shape = json.dumps(coordinates)
    )
    db.add(new_piece)
    db.commit()
    db.refresh(new_piece)
    return new_piece

@app.get("/{piece_name}/", status_code=status.HTTP_200_OK)
def get_piece(piece_name:str, db:Session=Depends(get_db)):
    piece = db.query(models.PieceBase).filter(models.PieceBase.name==piece_name).first()
    if not piece:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Piece name of {piece_name} is not available"
        )
    return piece

@app.post("/{piece_name}/", status_code=status.HTTP_201_CREATED)
def fr_piece(piece_name:str, db:Session=Depends(get_db)):
    piece = db.query(models.PieceBase).filter(models.PieceBase.name==piece_name).first()
    if not piece:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Piece name of {piece_name} is not available"
        )
    base_shape = json.loads(piece.base_shape)
    x_max = max(c["x"] for c in base_shape)
    y_max = max(c["y"] for c in base_shape)
    arr = np.zeros((x_max+1, y_max+1), dtype=int)
    for c in base_shape:
        x = c["x"]
        y = c["y"]
        arr[x,y] = 1
    l = rotate.flip_rot(arr)
    rotate.drop_dup(l)
    print(l)
    print(base_shape)
    fl_id = 0
    for arr in l:
        print(arr)
        for x,y in list(zip(*np.where(arr==1))):
            piece_fr = PieceFR(
                piecebase_id = piece.id,
                fliprot_id = fl_id,
                x = int(x),
                y = int(y),
            )
            print(piece.id, fl_id, x, y)
            db.add(piece_fr)
        fl_id += 1
    db.commit()
    db.refresh(piece_fr)

@app.get("/{piece_name}/{id}", status_code=status.HTTP_200_OK)
def fr(piece_name:str, id:int, db:Session=Depends(get_db)):
    query = db.query(PieceFR).join(PieceBase, PieceFR.piecebase_id==PieceBase.id).filter(PieceBase.name==piece_name)
    pieces = query.all()
    if not pieces:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Piece name of {piece_name} is not available"
        )
    piece = query.filter(PieceFR.fliprot_id==id).all()
    if not piece:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Index {id} is not found in flip-rotation of the piece {piece_name}"
        )
    return piece
