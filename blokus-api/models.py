from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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

class Field(Base):
    __tablename__ = "field"
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Integer)
    y = Column(Integer)
    value = Column(Integer, default=0)

class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    turn = Column(Integer, default=0)

class PlayerPieces(Base):
    __tablename__ = "player_pieces"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    piecebase_id = Column(Integer, ForeignKey('piece_base.id'))

class TurnControl(Base):
    __tablename__ = "turn_control"
    id = Column(Integer, primary_key=True, index=True)
    current_player_id = Column(Integer, ForeignKey('player.id'))
