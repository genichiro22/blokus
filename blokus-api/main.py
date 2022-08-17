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

from routes import piece

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))

URL = "http://localhost:8000/"
app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(piece.router)
# @app.get("/")
# def index():
#     return json.dumps(p_fr_base)

# @app.get("/")
# def index(request:Request):
#     return str(request.url)



@app.get("/field/")
def get_field(db:Session=Depends(get_db), status_code=status.HTTP_200_OK):
    field = db.query(Field).all()
    # print(field)
    return field

@app.get("/")
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
    update_player = {"turn": player.turn+1, "is_current_player": False}
    query.update(update_player)
    db.query(Player).filter(Player.id == put_piece.player%4+1).update({"is_current_player": True})
    db.query(PlayerPieces).filter(
        PlayerPieces.player_id==put_piece.player,
        PlayerPieces.piecebase_id==put_piece.piece_id
    ).delete()
    # new_turn = {"current_player_id": put_piece.player%4+1}
    # db.query(TurnControl).update(new_turn)
    db.commit()

@app.post("/player/")
def create_player(player_post:PlayerPost, db:Session=Depends(get_db)):
    new_player = Player(
        name = player_post.name,
        turn = player_post.turn,
        is_current_player = player_post.is_current,
    )
    db.add(new_player)
    db.commit()

def validate_whole(put_piece:PutPiece, db:Session=Depends(get_db)):
    validate_turn(put_piece, db)
    validate_posession(put_piece, db)
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

def validate_posession(put_piece:PutPiece, db:Session=Depends(get_db)):
    piece_id = put_piece.piece_id
    player = put_piece.player
    query = db.query(PlayerPieces).filter(
        PlayerPieces.player_id == player,
        PlayerPieces.piecebase_id == piece_id
    )
    if not query.all():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"You dont have piece with the id {piece_id}"
        )

def validate_turn(put_piece:PutPiece, db:Session=Depends(get_db)):
    current_player = db.query(Player).filter(
        Player.id == put_piece.player,
        Player.is_current_player == True
    ).all()
    if not current_player:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"Its not your turn"
        )

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