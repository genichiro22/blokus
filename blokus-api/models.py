from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class PieceBase(Base):
    __tablename__ = "piece_base"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    base_shape = Column(String)
    piece_fr = relationship("PieceFR", back_populates="base")
    
class PieceFR(Base):
    __tablename__ = "piece_fliprot"
    id = Column(Integer, primary_key=True, index=True)
    piecebase_id = Column(Integer, ForeignKey('piece_base.id'))
    fliprot_id = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)

    base = relationship('PieceBase', back_populates="piece_fr")
