from __future__ import annotations
import collections
from typing import Tuple, Optional
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


class Knight(Piece):
    def __init__(self, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        super().__init__(name, position, stats)
        self.item: Optional[Item] = None

    def equip(self, item: Item):
        self.item = item
        item.knight = self

    def unequip(self):
        self.item.knight = None
        self.item = None


class Item(Piece):
    def __init__(self, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        super().__init__(name, position, stats)
        self.knight: Optional[Knight] = None
