import models
from schemas import PutPiece
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
import itertools

class validation:
    def __init__(self, game:models.Game, put_piece:PutPiece, db:Session):
        self.game = game
        self.put_piece = put_piece
        self.db = db
        self.query = db.query(models.GamePlayer).join(models.Game).filter(
            models.GamePlayer.user_id == put_piece.user_id,
            models.Game.id == game.id
        )
        self.player = self.query.first().player
        self.field = self.game.field
        self.piece = db.query(models.PieceFR).filter(
            models.PieceFR.piecebase_id==self.put_piece.piece_id,
            models.PieceFR.fliprot_id==self.put_piece.fr_id
        ).all()
    
    def whole(self):
        self.turn()
        self.posession()
        self.inner_field()
        self.existence()
        if self.game.turn == self.player:
            self.first_turn()
        else:
            self.edge_condition()
            self.vertex_condition()

    def turn(self):
        # print("turn")
        if self.game.turn%4 != self.player%4:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = f"Its not your turn"
            )
    
    def posession(self):
        piece_id = self.put_piece.piece_id
        query = self.db.query(models.PlayerPieces).join(models.Game).filter(
            models.Game.id == self.game.id,
            models.PlayerPieces.player == self.player,
            models.PlayerPieces.piecebase_id == piece_id
        )
        if not query.all():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = f"You dont have piece with the id {piece_id}"
            )
    
    def inner_field(self):
        self.coordinates = [
            {
                "x": self.put_piece.coordinate.x + e.x,
                "y": self.put_piece.coordinate.y + e.y
            }
            for e in self.piece
        ]
        if any(any((c["x"]>=20,c["y"]>=20)) for c in self.coordinates):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "Not in field"
            )
    
    def existence(self):
        check = [
            {
                (c["x"], c["y"]): self.db.query(models.GameField).join(models.Game).filter(
                    models.GameField.x == c["x"],
                    models.GameField.y == c["y"],
                    models.Game.id == self.game.id
                ).first().player == 0
            }
            for c in self.coordinates
        ]
        if not all(all(e.values()) for e in check):
            l = [str(list(e.keys())[0]) for e in check if not all(e.values())]
            # print(l)
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = f"(x,y) = {', '.join(l)} already filled"
            )
    
    def first_turn(self):
        pc_dict = {1:(0,0), 2:(19,0), 3:(19,19), 4:(0,19)}
        x = pc_dict[self.player][0]
        y = pc_dict[self.player][1]
        l = [(c["x"]==x and c["y"]==y) for c in self.coordinates]
        if not any(l):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "First turn requirement not satisfied"
            )
    
    def vertex_condition(self):
        valid = False
        for c_dic, dx, dy in itertools.product(self.coordinates,(-1,1),(-1,1)):
            x = c_dic["x"]+dx
            y = c_dic["y"]+dy
            c = self.db.query(models.GameField).join(models.Game).filter(
                models.GameField.x==x,
                models.GameField.y==y,
                models.GameField.player == self.player,
                models.Game.id == self.game.id
            ).all()
            if not c:
                pass
            else:
                valid = True
        if not valid:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "Vertex condition not satisfied"
            )
    
    def edge_condition(self):
        for c_dic in self.coordinates:
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                x = c_dic["x"]+dx
                y = c_dic["y"]+dy
                query = self.db.query(models.GameField).join(models.Game).filter(
                    models.GameField.x==x,
                    models.GameField.y==y,
                    models.Game.id == self.game.id,
                    models.GameField.player == self.player
                ).all()
                if query:
                    raise HTTPException(
                        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail = "Edge condition not satisfied"
                    )
