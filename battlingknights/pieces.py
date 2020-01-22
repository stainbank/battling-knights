import collections
from typing import Tuple
from dataclasses import dataclass


class Piece():
    def __init__(self, name: str, position: Tuple[int, int]):
        self.name = name
        self.position = Position(*position)


@dataclass
class Position():
    row: int
    col: int
