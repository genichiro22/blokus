import models
from schemas import PiecePost
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
import numpy as np
import json

def create_piece(piece:PiecePost, db:Session):
    coordinates = [{"x":c.x, "y":c.y} for c in piece.base_shape]
    new_piece = models.PieceBase(
        name = piece.name,
        base_shape = json.dumps(coordinates)
    )
    db.add(new_piece)
    db.commit()
    db.refresh(new_piece)
    # print(new_piece.id)
    return new_piece

def read_piece(piece_name:str, db:Session):
    piece = db.query(models.PieceBase).filter(models.PieceBase.name==piece_name).first()
    if not piece:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Piece name of {piece_name} is not available"
        )
    return piece

def fr_all(db:Session):
    pieces = db.query(models.PieceBase).all()
    for p in pieces:
        # print(p.name)
        fr_piece(p.name, db)
    return "done"

# @app.post("/pieces/{piece_name}/", status_code=status.HTTP_201_CREATED)
def fr_piece(piece_name:str, db:Session):
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
    l = flip_rot(arr)
    drop_dup(l)
    # print(l)
    # print(base_shape)
    fl_id = 0
    for arr in l:
        # print(arr)
        for x,y in list(zip(*np.where(arr==1))):
            piece_fr = models.PieceFR(
                piecebase_id = piece.id,
                fliprot_id = fl_id,
                x = int(x),
                y = int(y),
            )
            # print(piece.id, fl_id, x, y)
            db.add(piece_fr)
        fl_id += 1
    db.commit()
    db.refresh(piece_fr)

def fr(piece_name:str, id:int, db:Session):
    query = db.query(models.PieceFR).join(models.PieceBase, models.PieceFR.piecebase_id==models.PieceBase.id).filter(models.PieceBase.name==piece_name)
    pieces = query.all()
    if not pieces:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Piece name of {piece_name} is not available"
        )
    piece = query.filter(models.PieceFR.fliprot_id==id).all()
    if not piece:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Index {id} is not found in flip-rotation of the piece {piece_name}"
        )
    return piece

def flip_rot(p):
    res = []
    p = np.array(p)
    for i in range(4):
        p_ = np.rot90(p)
        q_ = np.flipud(p_)
        res.append(p_)
        res.append(q_)
        p = p_
    return res

def drop_dup(l):
    while True:
        # print("current", l)
        n = len(l)
        loop=False
        for i in range(n):
            for j in range(n):
                a = tuple([tuple(e) for e in l[i]])
                b = tuple([tuple(e) for e in l[j]])
                if i>j and a==b:
                    del l[i]
                    loop = True
                    break
            else:
                continue
            break
        if not loop:
            break