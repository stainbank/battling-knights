from __future__ import annotations
import collections
from typing import Tuple, Optional
from dataclasses import dataclass
import enum


class Piece():
    def __init__(self, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        self.name = name
        self.position = Position(*position)
        self._stats = Stats(*stats)

    @property
    def attack(self):
        return self._stats.attack

    @property
    def defense(self):
        return self._stats.defense

    def move(self, direction: Direction):
        self.position += direction.value


@dataclass
class Position():
    row: int
    col: int

    def __add__(self, other: Position):
        return Position(self.row + other.row, self.col + other.col)


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

    @property
    def attack(self):
        return super().attack + self.item.attack

    @property
    def defense(self):
        return super().defense + self.item.defense


class Item(Piece):
    def __init__(self, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        super().__init__(name, position, stats)
        self.knight: Optional[Knight] = None


class Direction(enum.Enum):
    NORTH = Position(-1, 0)
    EAST = Position(0, 1)
    SOUTH = Position(1, 0)
    WEST = Position(0, -1)
