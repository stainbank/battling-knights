import pytest
from battlingknights.pieces import (Piece, Knight, Item, Direction, Status,
                                    InvalidMoveException)
from battlingknights.game import Arena


ARBITRARY_POSITION = (0, 1)
ARBITRARY_STATS = (2, 3)


@pytest.fixture
def knight():
    return Knight('Shyamalan', ARBITRARY_POSITION, ARBITRARY_STATS)


@pytest.fixture
def item():
    return Item('Panaflex Millenium', ARBITRARY_POSITION, ARBITRARY_STATS)


def test_piece_created_with_position():
    row, col = position = (2, 3)
    piece = Piece('Eigen', position, ARBITRARY_STATS)
    assert piece.position.row == row
    assert piece.position.col == col


def test_piece_created_with_stats():
    attack, defense = stats = (2, 3)
    piece = Piece('Pearson', ARBITRARY_POSITION, stats)
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


def test_equipped_knight_ignores_item(knight, item):
    other_item = Item('Banana Bomb', knight.position, ARBITRARY_STATS)
    knight.equip(item)
    knight.equip(other_item)
    assert knight.item is item


def test_knight_unequip_item(knight, item):
    knight.equip(item)
    knight.unequip()
    assert knight.item is None
    assert item.knight is None


def test_knight_gains_item_bonus(knight):
    item_attack, item_defense = item_stats = (4, 5)
    knight_attack, knight_defense = knight.attack, knight.defense
    item = Item('Roland', ARBITRARY_POSITION, item_stats)
    knight.equip(item)
    assert knight.attack == knight_attack + item_attack
    assert knight.defense == knight_defense + item_defense


def test_knight_position_updates_on_move():
    row, col = original_position = (0, 0)
    knight = Knight('Moves', original_position, ARBITRARY_STATS)
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
    knight = Knight('Hunter', position, ARBITRARY_STATS)
    item = Item('Fist', position, ARBITRARY_STATS)
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
    towards_water = {
            Direction.NORTH: origin,
            Direction.EAST: limits,
            Direction.SOUTH: limits,
            Direction.WEST: origin,
    }
    for direction, position in towards_water.items():
        knight = Knight('Sterling', position, ARBITRARY_STATS)
        knight.move(direction, limits)
        assert knight.status == Status.DROWNED
        assert knight.position is None


def test_knight_throws_item_to_bank_after_falling_off():
    original_position = limits = (7, 7)
    knight = Knight('Sterling', original_position, ARBITRARY_STATS)
    item = Item('Luckies', original_position, ARBITRARY_STATS)
    knight.equip(item)
    knight.move(Direction.SOUTH, limits)
    assert knight.item is None
    assert item.knight is None
    assert item.position == original_position
    assert (knight.attack, knight.defense) == (0, 0)


def test_knight_dies_when_killed(knight):
    knight.die()
    assert knight.status == Status.DEAD
    assert (knight.attack, knight.defense) == (0, 0)


def test_knight_drops_item_when_killed(knight, item):
    knight.equip(item)
    knight.die()
    assert knight.item is None
    assert item.knight is None


def test_knight_stays_on_tile_when_killed(knight):
    position = knight.position
    knight.die()
    assert knight.position == position


def test_unalive_knights_cannot_move(knight):
    knight.die()
    with pytest.raises(InvalidMoveException):
        knight.move(Direction.NORTH)


def test_attacking_knight_kills_weaker_knight(knight):
    weaker_stats = (knight.defense, knight.attack - 1)
    weaker_knight = Knight('Robin', ARBITRARY_POSITION, weaker_stats)
    knight.attack_knight(weaker_knight)
    _test_battle_outcome(winner=knight, loser=weaker_knight)


def test_attacking_knight_killed_by_stronger_knight(knight):
    stronger_stats = (knight.defense, knight.attack + 1)
    stronger_knight = Knight('Robin', ARBITRARY_POSITION, stronger_stats)
    knight.attack_knight(stronger_knight)
    _test_battle_outcome(winner=stronger_knight, loser=knight)


def test_attacking_knight_kills_equal_knight(knight):
    """The suprise bonus should win out."""
    inverted_stats = (knight.defense, knight.attack)
    equal_knight = Knight('Nalamayhs', ARBITRARY_POSITION, inverted_stats)
    knight.attack_knight(equal_knight)
    _test_battle_outcome(winner=knight, loser=equal_knight)


def _test_battle_outcome(winner, loser):
    assert winner.status == Status.LIVE
    assert loser.status == Status.DEAD
