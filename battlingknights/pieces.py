from __future__ import annotations
import collections
from typing import Tuple, Optional, Union, Any
from dataclasses import dataclass
import enum

from battlingknights import game


class Piece():
    def __init__(self, arena: game.Arena, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        self.arena: game.Arena = arena
        self.name: str = name
        self.position: Optional[Position] = Position(*position)
        self._stats: Stats = Stats(*stats)

    @property
    def attack(self):
        return self._stats.attack

    @property
    def defense(self):
        return self._stats.defense

    def move(self, direction: Direction):
        new_position = self.position + direction.value
        if not new_position.in_limits(self.arena.limits):
            raise OutsideLimitsException(
                f'Position {self} outside limits {self.arena.limits}')
        self.position = new_position


@dataclass
class Position():
    row: int
    col: int

    def __add__(self, other: Union[Position, Tuple[int, int]]):
        row_change, col_change = other
        return Position(self.row + row_change, self.col + col_change)

    def __eq__(self, other: Any):
        try:
            row, col = other
        except(TypeError, ValueError):
            return False
        return all([self.row == row, self.col == col])

    def __iter__(self):
        return iter((self.row, self.col))

    def in_limits(self, limits: Position):
        return all([
            0 <= self.row <= limits.row,
            0 <= self.col <= limits.col,
        ])


@dataclass
class Stats():
    attack: int
    defense: int


class Knight(Piece):
    def __init__(self, arena: game.Arena, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        super().__init__(arena, name, position, stats)
        self.status: Status = Status.LIVE
        self.item: Optional[Item] = None

    def equip(self, item: Item):
        self.item = item
        item.knight = self

    def unequip(self):
        if self.item:
            self.item.knight = None
            self.item = None

    @property
    def attack(self):
        return super().attack + self.item.attack

    @property
    def defense(self):
        return super().defense + self.item.defense

    def move(self, direction: Direction):
        try:
            super().move(direction)
            if self.item:
                self.item.move(direction)
        except OutsideLimitsException:
            self._fall_off()

    def _fall_off(self):
        self.unequip()
        self.status = Status.DROWNED
        self.position = None


class Item(Piece):
    def __init__(self, arena: game.Arena, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        super().__init__(arena, name, position, stats)
        self.knight: Optional[Knight] = None


class Direction(enum.Enum):
    NORTH = Position(-1, 0)
    EAST = Position(0, 1)
    SOUTH = Position(1, 0)
    WEST = Position(0, -1)


class Status(enum.Enum):
    LIVE = enum.auto()
    DROWNED = enum.auto()


class BattlingKnightsException(Exception):
    pass


class OutsideLimitsException(BattlingKnightsException):
    pass
