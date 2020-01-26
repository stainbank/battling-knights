from __future__ import annotations
from typing import Tuple, Set, Union

from .pieces import Position, Piece, Knight, Item
from .exceptions import InvalidGameStateException


class Arena:
    def __init__(self, limits: Tuple[int, int]):
        self.limits: Position = Position(*limits)
        self.pieces: Set[Piece] = set()

    def set_pieces(self, *pieces):
        for piece in pieces:
            piece.position.raise_if_invalid(self.limits)
        self.pieces = self.pieces.union(pieces)

    def tile(self, position: Union[Position, Tuple[int, int]]):
        position = Position(*position)
        position.raise_if_invalid(self.limits)
        return Tile(self, position)


class Tile:
    def __init__(self, arena: Arena, position: Position):
        self.arena = arena
        self.position = position

    @property
    def items(self):
        return self._get_pieces(Item)

    @property
    def knight(self):
        knights = self._get_pieces(Knight)
        if len(knights) > 1:
            msg = f'Knights cannot superpose: {knights}.'
            raise InvalidGameStateException(msg)
        return knights.pop() if knights else None

    def _get_pieces(self, piece_type: type):
        pieces = {piece for piece in self.arena.pieces
                  if isinstance(piece, piece_type)
                  and piece.position == self.position}
        return pieces
