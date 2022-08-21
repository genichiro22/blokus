from pydantic import BaseModel
from typing import List, Optional

class Coordinate(BaseModel):
    x: int
    y: int
    class Config:
        orm_mode=True

class PiecePost(BaseModel):
    name: str
    base_shape: List[Coordinate]
    class Config:
        orm_mode=True

class FieldPost(BaseModel):
    player: int
    coordinates: List[Coordinate]
    class Config:
        orm_mode=True

class PutPiece(BaseModel):
    player: int
    # turn: int
    piece_id: int
    fr_id: int
    coordinate: Coordinate
    class Config:
        orm_mode=True

class PlayerPost(BaseModel):
    name: str
    pwd: str
    is_first: bool
    class Config:
        orm_mode=True