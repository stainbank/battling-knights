import pytest
from battlingknights.game import Arena
from battlingknights.pieces import Piece, Position, OutsideLimitsException
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
