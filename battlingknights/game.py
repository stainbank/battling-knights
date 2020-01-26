from __future__ import annotations
from typing import Tuple, Set, Union
from battlingknights.pieces import Position, Piece


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
        return Tile(position)


class Tile:
    def __init__(self, position: Position):
        self.position = position
