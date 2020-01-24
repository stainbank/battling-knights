import pytest
from battlingknights.pieces import Piece, Knight, Item, Direction


@pytest.fixture
def knight():
    return Knight('Shyamalan', (0, 1), (2, 3))


@pytest.fixture
def item():
    return Item('Panaflex Millenium', (0, 1), (2, 3))


def test_piece_created_with_position():
    row, col = position = (2, 3)
    piece = Piece('Example', position, (0, 0))
    assert piece.position.row == row
    assert piece.position.col == col


def test_piece_created_with_stats():
    attack, defense = stats = (2, 3)
    piece = Piece('Example', (0, 0), stats)
    assert piece.attack == attack
    assert piece.defense == defense


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


def test_knight_gains_item_bonus():
    position = (0, 0)
    knight_attack, knight_defense = knight_stats = (2, 3)
    item_attack, item_defense = item_stats = (4, 5)
    knight = Knight('Elgato', position, knight_stats)
    item = Item('Roland', position, item_stats)
    knight.equip(item)
    assert knight.attack == knight_attack + item_attack
    assert knight.defense == knight_defense + item_defense


def test_knight_position_updates_on_move():
    row, col = original_position = (0, 0)
    knight = Knight('Moves', original_position, (0, 0))
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


def test_equipped_item_moves_with_knight():
    position = (0, 0)
    knight = Knight('Hunter', position, (0, 0))
    item = Item('Fist', position, (0, 0))
    knight.equip(item)
    knight.move(Direction.EAST)
    assert knight.position == item.position
    knight.move(Direction.SOUTH)
    assert knight.position == item.position
    knight.move(Direction.WEST)
    assert knight.position == item.position
    knight.move(Direction.NORTH)
    assert knight.position == item.position
