from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class PieceName(Base):
    __tablename__ = "piecename"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
class Piece(Base):
    __tablename__ = "piece_fliprot"
    id = Column(Integer, primary_key=True, index=True)
    piecename_id = Column(Integer)
    fliprot_id = Column(Integer)
    x = Column(Boolean)
    y = Column(Boolean)