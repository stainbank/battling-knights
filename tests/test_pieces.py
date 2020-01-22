import pytest
from battlingknights.pieces import Piece

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
