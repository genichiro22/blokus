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
