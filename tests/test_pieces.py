import pytest
from battlingknights.pieces import Piece, Knight, Item


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
    assert piece.stats.attack == attack
    assert piece.stats.defense == defense


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
