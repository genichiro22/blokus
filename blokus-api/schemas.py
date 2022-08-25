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
    user_id: int
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

class NewUser(BaseModel):
    name: str
    pwd: str
    class Config:
        orm_mode=True

class UserToPlayer(BaseModel):
    player: int
    user_id: int

class Login(BaseModel):
    user_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None