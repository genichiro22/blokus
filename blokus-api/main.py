from fastapi import FastAPI, Depends, Query, status, Response, HTTPException, Request
from fastapi.responses import HTMLResponse
from schemas import PiecePost, FieldPost, PutPiece
from models import PieceBase, PieceFR, Field, Player, PlayerPieces
# from . import models
from database import engine, sessionLocal, Base, get_db
from sqlalchemy.orm import Session
from jinja2 import Template, Environment, FileSystemLoader
# from .piece import rotate
import json
import numpy as np
from rotate import rotate
import itertools
import requests
# pieces_fr = rotate.pieces_fr
# p_fr_base = {}

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))

URL = "http://localhost:8000/"
app = FastAPI()
Base.metadata.create_all(engine)
# @app.get("/")
# def index():
#     return json.dumps(p_fr_base)
@app.get("/")
def index(request:Request):
    return str(request.url)

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
    # print(field)
    return field
'''
@app.get("/field/render/")
def ged_rendered_field(db:Session=Depends(get_db)):
    l = []
    for y in range(20):
        ly=[]
        for x in range(20):
            e = db.query(Field).filter(Field.x==x, Field.y==y)
            p = e.first().value
            # print(p)
            append_str = str(p) if p!=0 else " "
            ly.append(append_str)
        l.append(ly)
    # print(l)
    # for i in range(len(l)):
        # l[i] = "|".join(l[i])
    s = "|"+"<br>|".join(["|".join(e) for e in l])
    s2 = '<font face="ＭＳ ゴシック">' + s + '</font>'
    return HTMLResponse(content=s2, status_code=200)
'''

@app.get("/field/render/")
def get_rendered_field_by_jinja2(request:Request,db:Session=Depends(get_db)):
    url = URL + "field/"
    txt = requests.get(url).json()
    tmpl = env.get_template('render.j2')
    c = tmpl.render(field=txt)
    return HTMLResponse(content=c)

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
        current_field = db.query(Field).filter(Field.x == c.x, Field.y == c.y)
        field = {
            "x": c.x,
            "y": c.y,
            "value": player
        }
        current_field.update(field)
    db.commit()
    return "updated"

@app.put("/field/piece/")
def put_piece_to_field(put_piece:PutPiece, db:Session=Depends(get_db)):
    # print(put_piece)
    # print(1)
    piece = db.query(PieceFR).filter(PieceFR.piecebase_id==put_piece.piece_id, PieceFR.fliprot_id==put_piece.fr_id).all()
    # print(piece)
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    # print(coordinates)
    validate_whole(put_piece, db)
    field_post = FieldPost(
        player=put_piece.player,
        coordinates=coordinates
    )
    update_field(field_post, db)
    query = db.query(Player).filter(Player.id == put_piece.player)
    player = query.first()
    update_player = {
        # "id": player.id,
        "turn": player.turn+1
    }
    query.update(update_player)
    db.commit()

def validate_whole(put_piece:PutPiece, db:Session=Depends(get_db)):
    if not validate_inner_field(put_piece,db):
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "Not in field"
        )
    ve = validate_existence(put_piece, db)
    if not all(all(e.values()) for e in ve):
        l = [str(list(e.keys())[0]) for e in ve if not all(e.values())]
        # print(l)
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"(x,y) = {', '.join(l)} already filled"
        )
    # print(validate_edge_condition(put_piece, db))
    player = db.query(Player).filter(Player.id == put_piece.player).first()
    if player.turn==0:
        if not validate_first_turn(put_piece, db):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "First turn requirement not satisfied"
            )
    else:
        vec = validate_edge_condition(put_piece, db)
        if not vec:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "Edge condition not satisfied"
            )
        vvc = validate_vertex_condition(put_piece, db)
        if not vvc:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "Vertex condition not satisfied"
            )

def validate_inner_field(put_piece:PutPiece, db:Session=Depends(get_db)):
    # valid = True
    piece = db.query(PieceFR).filter(PieceFR.piecebase_id==put_piece.piece_id, PieceFR.fliprot_id==put_piece.fr_id).all()
    # print(piece)
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    # print(coordinates)
    return not any(any((c["x"]>=20,c["y"]>=20)) for c in coordinates)

def validate_existence(put_piece:PutPiece, db:Session=Depends(get_db)):
    piece = db.query(PieceFR).filter(PieceFR.piecebase_id==put_piece.piece_id, PieceFR.fliprot_id==put_piece.fr_id).all()
    # print(piece)
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    existence = [
        {
            (c["x"], c["y"]): db.query(Field).filter(Field.x == c["x"], Field.y == c["y"]).first().value == 0
        }
        for c in coordinates
    ]
    return existence

def validate_vertex_condition(put_piece:PutPiece, db:Session=Depends(get_db)):
    valid = False
    piece = db.query(PieceFR).filter(PieceFR.piecebase_id==put_piece.piece_id, PieceFR.fliprot_id==put_piece.fr_id).all()
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    field = db.query(Field)
    for c_dic, dx, dy in itertools.product(coordinates,(-1,1),(-1,1)):
        x = c_dic["x"]+dx
        y = c_dic["y"]+dy
        query = field.filter(Field.x==x, Field.y==y).first()
        if not query:
            pass
        elif query.value == put_piece.player:
            valid = True
    return valid

def validate_edge_condition(put_piece:PutPiece, db:Session=Depends(get_db)):
    valid = True
    piece = db.query(PieceFR).filter(PieceFR.piecebase_id==put_piece.piece_id, PieceFR.fliprot_id==put_piece.fr_id).all()
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    field = db.query(Field)
    for c_dic in coordinates:
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x = c_dic["x"]+dx
            y = c_dic["y"]+dy
            query = field.filter(Field.x==x, Field.y==y).first()
            if not query:
                pass
            elif query.value == put_piece.player:
                valid = False
    return valid

def validate_first_turn(put_piece:PutPiece, db:Session=Depends(get_db)):
    player = put_piece.player
    piece = db.query(PieceFR).filter(PieceFR.piecebase_id==put_piece.piece_id, PieceFR.fliprot_id==put_piece.fr_id).all()
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    pc_dict = {1:(0,0), 2:(19,0), 3:(19,19), 4:(0,19)}
    x = pc_dict[player][0]
    y = pc_dict[player][1]
    l = [(c["x"]==x and c["y"]==y) for c in coordinates]
    return any(l)

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