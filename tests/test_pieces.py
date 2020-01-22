import pytest
from battlingknights.pieces import Piece

def test_piece_created_with_position():
    row, col = position = (2, 3)
    piece = Piece('Example', position)
    assert piece.position.row == row
    assert piece.position.col == col
