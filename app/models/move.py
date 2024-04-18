from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Move(Base):
    """
    Represents a single move in a game, including the x and y coordenate of the move.
    """

    __tablename__ = "moves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    is_machine_move = Column(Boolean, default=False, nullable=False)
    game = relationship("Game")
