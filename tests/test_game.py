import pytest
from unittest.mock import patch
from battlingknights.game import Arena
from battlingknights.pieces import Piece, Item, Knight, Position, Direction
from battlingknights.exceptions import (
        InvalidGameStateException, OutsideLimitsException)
from test_pieces import ARBITRARY_POSITION, ARBITRARY_STATS


@pytest.fixture
def arena():
    return Arena((7, 7))


@pytest.fixture
def invalid_position(arena):
    return Position(arena.limits.row + 1, arena.limits.col + 1)


def test_arena_sets_pieces(arena):
    positions = [ARBITRARY_POSITION, ARBITRARY_POSITION, arena.limits]
    pieces = {Piece(str(i), position, ARBITRARY_STATS)
              for i, position in enumerate(positions)}
    arena.set_pieces(*pieces)
    assert len(arena.pieces) == len(pieces)
    for piece in pieces:
        assert piece in arena.pieces


def test_arena_does_not_set_invalid_pieces(arena, invalid_position):
    bad_piece = Piece("Broken Butterfly", invalid_position, ARBITRARY_STATS)
    with pytest.raises(OutsideLimitsException):
        arena.set_pieces(bad_piece)


def test_tile_created_from_position(arena):
    position = (2, 3)
    tile = arena.tile(position)
    assert tile.position == position


def test_invalid_tile_not_created(arena, invalid_position):
    with pytest.raises(OutsideLimitsException):
        tile = arena.tile(invalid_position)


def test_tile_holds_pieces(arena):
    """Since pieces fetched dynamically, tile creation time wont matter."""
    position = (2, 3)
    tile = arena.tile(position)
    knight = Knight('Starboy', position, ARBITRARY_STATS)
    items = {Item(str(i), position, ARBITRARY_STATS) for i in range(2)}
    arena.set_pieces(knight, *items)
    assert tile.knight is knight
    assert len(tile.items) == len(items)
    for item in items:
        assert item in tile.items


def test_tile_holds_only_one_knight(arena):
    position = (2, 3)
    knights = {Knight(str(i), position, ARBITRARY_STATS) for i in range(2)}
    arena.set_pieces(*knights)
    with pytest.raises(InvalidGameStateException):
        tile = arena.tile(position)
        tile.knight


def test_empty_tile_holds_no_pieces(arena):
    position = (2, 3)
    empty_position = (3, 4)
    tile = arena.tile(empty_position)
    knight = Knight('Starboy', position, ARBITRARY_STATS)
    items = {Item(str(i), position, ARBITRARY_STATS) for i in range(2)}
    arena.set_pieces(knight, *items)
    assert not tile.items
    assert tile.knight is None


def test_knight_moves_on_instruction(arena):
    starting_position = (0, 0)
    knight = Knight('Merciless Ming', starting_position, ARBITRARY_STATS)
    arena.set_pieces(knight)
    arena.run_instruction(knight, Direction.SOUTH)
    assert knight.position == (1, 0)


def test_knight_equips_item_on_move(arena):
    starting_position = (0, 0)
    knight = Knight('Merciless Ming', starting_position, ARBITRARY_STATS)
    item = Item('Ming Vase', (0, 1), ARBITRARY_STATS)
    arena.set_pieces(knight, item)
    arena.run_instruction(knight, Direction.EAST)
    assert knight.item is item


def test_knights_fight_on_move(arena):
    knight = Knight('Marcus Junius', (0, 0), ARBITRARY_STATS)
    other_knight = Knight('Gaius Julius', (1, 0), ARBITRARY_STATS)
    arena.set_pieces(knight, other_knight)
    with patch.object(knight, 'attack_knight'):
        arena.run_instruction(knight, Direction.SOUTH)
        knight.attack_knight.assert_called_with(other_knight)
