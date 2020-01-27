from __future__ import annotations
from typing import Tuple, Set, Union, Optional, Callable

from .pieces import Piece, Knight, Item, Position, Direction
from .exceptions import InvalidGameStateException, InvalidMoveException


ChoosesItem = Callable[[Set[Item]], Optional[Item]]


class Arena:
    def __init__(self, limits: Tuple[int, int],
                 item_chooser: Optional[ChoosesItem] = None):
        self.limits: Position = Position(*limits)
        self.pieces: Set[Piece] = set()
        self.choose_item = item_chooser if item_chooser else _choose_any_item

    def set_pieces(self, *pieces):
        for piece in pieces:
            piece.position.raise_if_invalid(self.limits)
        self.pieces = self.pieces.union(pieces)

    def run_instruction(self, knight: Knight, direction: Direction):
        if knight.position is None:
            raise InvalidMoveException('Dead knights cannot move.')
        target: Tile = self.tile(knight.position + direction)
        defender: Optional[Knight] = target.knight
        item: Optional[Item] = self.choose_item(target.items)
        knight.move(direction)
        if item:
            knight.equip(item)
        if defender:
            knight.attack_knight(defender)
        # should an unequipped victor pick up his fallen enemies item?

    def tile(self, position: Union[Position, Tuple[int, int]]):
        position = Position(*position)
        position.raise_if_invalid(self.limits)
        return Tile(self, position)


def _choose_any_item(items: Set[Item]) -> Optional[Item]:
    """Default item chooser returning arbitrary item."""
    try:
        return items.pop()
    except KeyError:
        return None


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
