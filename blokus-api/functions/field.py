import models
from schemas import PutPiece, FieldPost
from sqlalchemy.orm import Session
from fastapi import status, HTTPException


def read(db:Session, status_code=status.HTTP_200_OK):
    field = db.query(models.Field).all()
    # print(field)
    return field

def create(db:Session, status_code=status.HTTP_201_CREATED):
    for x in range(20):
        for y in range(20):
            plot = models.Field(x=x, y=y)
            db.add(plot)
    db.commit()
    db.refresh(plot)
    return

def update(field_update:FieldPost, db:Session, status_code=status.HTTP_200_OK):
    player = field_update.player
    for c in field_update.coordinates:
        current_field = db.query(models.Field).filter(models.Field.x == c.x, models.Field.y == c.y)
        field = {
            "x": c.x,
            "y": c.y,
            "value": player
        }
        current_field.update(field)
    db.commit()
    return "updated"

def put_piece(put_piece:PutPiece, db:Session):
    # print(put_piece)
    # print(1)
    piece = db.query(models.PieceFR).filter(models.PieceFR.piecebase_id==put_piece.piece_id, models.PieceFR.fliprot_id==put_piece.fr_id).all()
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
    update(field_post, db)
    query = db.query(models.Player).filter(models.Player.id == put_piece.player)
    player = query.first()
    update_player = {"turn": player.turn+1, "is_current_player": False}
    query.update(update_player)
    db.query(models.Player).filter(models.Player.id == put_piece.player%4+1).update({"is_current_player": True})
    db.query(models.PlayerPieces).filter(
        models.PlayerPieces.player_id==put_piece.player,
        models.PlayerPieces.piecebase_id==put_piece.piece_id
    ).delete()
    # new_turn = {"current_player_id": put_piece.player%4+1}
    # db.query(TurnControl).update(new_turn)
    db.commit()



def validate_whole(put_piece:PutPiece, db:Session):
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
    player = db.query(models.Player).filter(models.Player.id == put_piece.player).first()
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

def validate_inner_field(put_piece:PutPiece, db:Session):
    # valid = True
    piece = db.query(models.PieceFR).filter(models.PieceFR.piecebase_id==put_piece.piece_id, models.PieceFR.fliprot_id==put_piece.fr_id).all()
    # print(piece)
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    # print(coordinates)
    return not any(any((c["x"]>=20,c["y"]>=20)) for c in coordinates)

def validate_existence(put_piece:PutPiece, db:Session):
    piece = db.query(models.PieceFR).filter(models.PieceFR.piecebase_id==put_piece.piece_id, models.PieceFR.fliprot_id==put_piece.fr_id).all()
    # print(piece)
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    existence = [
        {
            (c["x"], c["y"]): db.query(models.Field).filter(models.Field.x == c["x"], models.Field.y == c["y"]).first().value == 0
        }
        for c in coordinates
    ]
    return existence

def validate_vertex_condition(put_piece:PutPiece, db:Session):
    valid = False
    piece = db.query(models.PieceFR).filter(models.PieceFR.piecebase_id==put_piece.piece_id, models.PieceFR.fliprot_id==put_piece.fr_id).all()
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    field = db.query(models.Field)
    for c_dic, dx, dy in itertools.product(coordinates,(-1,1),(-1,1)):
        x = c_dic["x"]+dx
        y = c_dic["y"]+dy
        query = field.filter(models.Field.x==x, models.Field.y==y).first()
        if not query:
            pass
        elif query.value == put_piece.player:
            valid = True
    return valid

def validate_edge_condition(put_piece:PutPiece, db:Session):
    valid = True
    piece = db.query(models.PieceFR).filter(models.PieceFR.piecebase_id==put_piece.piece_id, models.PieceFR.fliprot_id==put_piece.fr_id).all()
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    field = db.query(models.Field)
    for c_dic in coordinates:
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x = c_dic["x"]+dx
            y = c_dic["y"]+dy
            query = field.filter(models.Field.x==x, models.Field.y==y).first()
            if not query:
                pass
            elif query.value == put_piece.player:
                valid = False
    return valid

def validate_first_turn(put_piece:PutPiece, db:Session):
    player = put_piece.player
    piece = db.query(models.PieceFR).filter(models.PieceFR.piecebase_id==put_piece.piece_id, models.PieceFR.fliprot_id==put_piece.fr_id).all()
    coordinates = [
        {"x":put_piece.coordinate.x + e.x, "y":put_piece.coordinate.y + e.y}
        for e in piece
    ]
    pc_dict = {1:(0,0), 2:(19,0), 3:(19,19), 4:(0,19)}
    x = pc_dict[player][0]
    y = pc_dict[player][1]
    l = [(c["x"]==x and c["y"]==y) for c in coordinates]
    return any(l)

def validate_posession(put_piece:PutPiece, db:Session):
    piece_id = put_piece.piece_id
    player = put_piece.player
    query = db.query(models.PlayerPieces).filter(
        models.PlayerPieces.player_id == player,
        models.PlayerPieces.piecebase_id == piece_id
    )
    if not query.all():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"You dont have piece with the id {piece_id}"
        )

def validate_turn(put_piece:PutPiece, db:Session):
    current_player = db.query(models.Player).filter(
        models.Player.id == put_piece.player,
        models.Player.is_current_player == True
    ).all()
    if not current_player:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"Its not your turn"
        )