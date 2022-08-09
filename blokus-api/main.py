from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import PiecePost, FieldPost
from .models import PieceBase, PieceFR, Field
# from . import models
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

@app.post("/pieces/", status_code=status.HTTP_201_CREATED)
def post_piece(piece:PiecePost, db:Session=Depends(get_db),):
    # print(base_shape)
    # print(piece.base_shape)
    coordinates = [{"x":c.x, "y":c.y} for c in piece.base_shape]
    # print(coordinates)
    # print(json.dumps(coordinates))
    # base_shape = piece.base_shape
    new_piece = PieceBase(
        name = piece.name,
        base_shape = json.dumps(coordinates)
    )
    db.add(new_piece)
    db.commit()
    db.refresh(new_piece)
    print(new_piece.id)
    return new_piece

@app.get("/pieces/{piece_name}/", status_code=status.HTTP_200_OK)
def get_piece(piece_name:str, db:Session=Depends(get_db)):
    piece = db.query(PieceBase).filter(PieceBase.name==piece_name).first()
    if not piece:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Piece name of {piece_name} is not available"
        )
    return piece

@app.post("/pieces/all/")
def fr_all(db:Session=Depends(get_db)):
    pieces = db.query(PieceBase).all()
    for p in pieces:
        print(p.name)
        fr_piece(p.name, db)
    return "done"

# @app.post("/pieces/{piece_name}/", status_code=status.HTTP_201_CREATED)
def fr_piece(piece_name:str, db:Session=Depends(get_db)):
    piece = db.query(PieceBase).filter(PieceBase.name==piece_name).first()
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

@app.get("/pieces/{piece_name}/{id}", status_code=status.HTTP_200_OK)
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

@app.get("/field/")
def get_field(db:Session=Depends(get_db), status_code=status.HTTP_200_OK):
    field = db.query(Field).all()
    return field

@app.post("/field/")
def post_field(db:Session=Depends(get_db), status_code=status.HTTP_201_CREATED):
    for x in range(20):
        for y in range(20):
            plot = Field(x=x, y=y)
            db.add(plot)
    db.commit()
    db.refresh(plot)
    return

@app.put("/field/")
def update_field(field_update:FieldPost, db:Session=Depends(get_db), status_code=status.HTTP_200_OK):
    player = field_update.player
    for c in field_update.coordinates:
        current_field = db.query(Field).filter(Field.x == c.x).filter(Field.y == c.y)
        field = {
            "x": c.x,
            "y": c.y,
            "value": player
        }
        current_field.update(field)
    db.commit()
    return "updated"