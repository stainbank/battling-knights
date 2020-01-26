from __future__ import annotations
import collections
from typing import Tuple, Optional, Union, Any
from dataclasses import dataclass
import enum


class Piece():
    def __init__(self, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        self.name: str = name
        self.position: Optional[Position] = Position(*position)
        self._stats: Stats = Stats(*stats)

    @property
    def attack(self):
        return self._stats.attack

    @property
    def defense(self):
        return self._stats.defense

    def move(self, direction: Direction, limits: Optional[Position] = None):
        new_position = self.position + direction.value
        if limits:
            new_position.raise_if_invalid(limits)
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

    def raise_if_invalid(self, limits: Position):
        in_limits = all([
            0 <= self.row <= limits.row,
            0 <= self.col <= limits.col,
        ])
        if not in_limits:
            raise OutsideLimitsException(
                f'Position {self} outside limits {limits}')


@dataclass
class Stats():
    attack: int
    defense: int


class Knight(Piece):
    def __init__(self, name: str, position: Tuple[int, int],
                 stats: Tuple[int, int]):
        super().__init__(name, position, stats)
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
        item_attack = self.item.attack if self.item else 0
        return super().attack + item_attack

    @property
    def defense(self):
        item_defense = self.item.defense if self.item else 0
        return super().defense + item_defense

    def move(self, direction: Direction, limits: Optional[Position] = None):
        if self.status != Status.LIVE:
            raise InvalidMoveException('Dead Knights cannot move')
        try:
            super().move(direction, limits)
            if self.item:
                self.item.move(direction)
        except OutsideLimitsException:
            self._fall_off()

    def _fall_off(self):
        self.die()
        self.position = None
        self.status = Status.DROWNED

    def die(self):
        self.unequip()
        self._stats = Stats(0, 0)
        self.status = Status.DEAD


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


class Status(enum.Enum):
    LIVE = enum.auto()
    DROWNED = enum.auto()
    DEAD = enum.auto()


class BattlingKnightsException(Exception):
    pass


class InvalidMoveException(BattlingKnightsException):
    pass


class OutsideLimitsException(InvalidMoveException):
    pass
