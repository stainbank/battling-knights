from __future__ import annotations
from typing import Tuple
from battlingknights import pieces


class Arena:
    def __init__(self, limits: Tuple[int, int]):
        self.limits = pieces.Position(*limits)
