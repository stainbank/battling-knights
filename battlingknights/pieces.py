import collections
from typing import Tuple
from dataclasses import dataclass


class Piece():
    def __init__(self, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        self.name = name
        self.position = Position(*position)
        self.stats = Stats(*stats)


@dataclass
class Position():
    row: int
    col: int


@dataclass
class Stats():
    attack: int
    defense: int
