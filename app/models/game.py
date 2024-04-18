import math

from sqlalchemy import Column, Integer, Sequence
from sqlalchemy.orm import relationship

from .base import Base
from .move import Move


class Game(Base):
    """
    Represents a game entity where each game can have multiple moves.
    Each game is uniquely identified by an ID.
    """

    __tablename__ = "games"

    id = Column(Integer, Sequence("game_id_seq"), primary_key=True, autoincrement=True)
    moves = relationship(
        "Move",
        back_populates="game",
        order_by="Move.created_at.asc()",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def get_move(self, x: int, y: int) -> Move:
        for move in self.moves:
            if move.x == x and move.y == y:
                return move

    def machines_wins(self) -> bool:
        machine_moves = [m for m in self.moves if m.is_machine_move]
        return self._is_there_a_winner(machine_moves)

    def user_wins(self) -> bool:
        user_moves = [m for m in self.moves if not m.is_machine_move]
        return self._is_there_a_winner(user_moves)

    def _is_there_a_winner(self, moves: list[Move]) -> bool:
        for row in range(3):
            if sum([1 for m in moves if m.x == row]) == 3:
                return True

        for column in range(3):
            if sum([1 for m in moves if m.y == column]) == 3:
                return True

        if sum([1 for m in moves if m.x == m.y]) == 3 or sum(
            [1 for m in moves if m.x == math.abs(m.y - 2)]
        ):
            return True

    @property
    def completed(self):
        return self.user_wins() or self.machines_wins()

    @property
    def winner(self):
        if self.user_wins():
            return "user"
        if self.machines_wins():
            return "machine"
