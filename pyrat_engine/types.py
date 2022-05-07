from typing import Tuple

from enum import Enum

Coordinates = Tuple[int, int]


class Move(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    DID_NOT_MOVE = 4
