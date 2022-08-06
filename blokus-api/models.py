from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class PieceName(Base):
    __tablename__ = "piece_name"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    base_shape = Column(String)
    
class PieceFR(Base):
    __tablename__ = "piece_fliprot"
    id = Column(Integer, primary_key=True, index=True)
    piecename_id = Column(Integer)
    fliprot_id = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)