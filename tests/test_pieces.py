import pytest
from battlingknights.pieces import Piece, Knight, Item, Direction, Status
from battlingknights.game import Arena


@pytest.fixture
def arena():
    return Arena((7, 7))


@pytest.fixture
def knight(arena):
    return Knight(arena, 'Shyamalan', (0, 1), (2, 3))


@pytest.fixture
def item(arena):
    return Item(arena, 'Panaflex Millenium', (0, 1), (2, 3))


def test_piece_created_with_position(arena):
    row, col = position = (2, 3)
    piece = Piece(arena, 'Example', position, (0, 0))
    assert piece.position.row == row
    assert piece.position.col == col


def test_piece_created_with_stats(arena):
    attack, defense = stats = (2, 3)
    piece = Piece(arena, 'Example', (0, 0), stats)
    assert piece.attack == attack
    assert piece.defense == defense


def test_knight_born_alive(knight):
    assert knight.status == Status.LIVE


def test_knight_equips_item(knight, item):
    assert knight.item is None
    assert item.knight is None
    knight.equip(item)
    assert knight.item is item
    assert item.knight is knight


def test_knight_unequip_item(knight, item):
    knight.equip(item)
    knight.unequip()
    assert knight.item is None
    assert item.knight is None


def test_knight_gains_item_bonus(arena):
    position = (0, 0)
    knight_attack, knight_defense = knight_stats = (2, 3)
    item_attack, item_defense = item_stats = (4, 5)
    knight = Knight(arena, 'Elgato', position, knight_stats)
    item = Item(arena, 'Roland', position, item_stats)
    knight.equip(item)
    assert knight.attack == knight_attack + item_attack
    assert knight.defense == knight_defense + item_defense


def test_knight_position_updates_on_move(arena):
    row, col = original_position = (0, 0)
    knight = Knight(arena, 'Moves', original_position, (0, 0))
    knight.move(Direction.EAST)
    assert knight.position.row == 0
    assert knight.position.col == 1
    knight.move(Direction.SOUTH)
    assert knight.position.row == 1
    assert knight.position.col == 1
    knight.move(Direction.WEST)
    assert knight.position.row == 1
    assert knight.position.col == 0
    knight.move(Direction.NORTH)
    assert knight.position.row == row
    assert knight.position.col == col


def test_equipped_item_moves_with_knight(arena):
    position = (0, 0)
    knight = Knight(arena, 'Hunter', position, (0, 0))
    item = Item(arena, 'Fist', position, (0, 0))
    knight.equip(item)
    knight.move(Direction.EAST)
    assert knight.position == item.position
    knight.move(Direction.SOUTH)
    assert knight.position == item.position
    knight.move(Direction.WEST)
    assert knight.position == item.position
    knight.move(Direction.NORTH)
    assert knight.position == item.position


def test_knight_falls_off_edge_and_drowns():
    origin, limits = (0, 0), (7, 7)
    arena = Arena(limits)
    towards_water = {
            Direction.NORTH: origin,
            Direction.EAST: limits,
            Direction.SOUTH: limits,
            Direction.WEST: origin,
    }
    for direction, position in towards_water.items():
        knight = Knight(arena, 'Sterling', position, (0, 0))
        knight.move(direction)
        assert knight.status == Status.DROWNED
        assert knight.position is None
