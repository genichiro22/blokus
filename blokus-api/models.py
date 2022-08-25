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

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    raw_pwd = Column(String)

class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, index=True)
    turn = Column(Integer, default=1)

    field = relationship("GameField", back_populates="game")
    pieces = relationship("PlayerPieces", back_populates="game")

class GameField(Base):
    __tablename__ = "game_field"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    x = Column(Integer)
    y = Column(Integer)
    player = Column(Integer, default=0)

    game = relationship("Game", back_populates="field")

class GamePlayer(Base):
    __tablename__ = "game_player"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    player = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))


class PlayerPieces(Base):
    __tablename__ = "player_pieces"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    player = Column(Integer, ForeignKey('game_player.player'))
    piecebase_id = Column(Integer, ForeignKey('piece_base.id'))
    
    game = relationship("Game", back_populates="pieces")
