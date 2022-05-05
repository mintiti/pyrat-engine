from dataclasses import dataclass
from enum import Enum, IntEnum, unique
from typing import Tuple, Optional, List

from pyrat_engine.types import Coordinates


@unique
class CheeseMode(IntEnum):
    SYMMETRICAL = 0  # Force symmetrical cheeses
    ASYMMETRICAL = 1  # asymmetrical cheeses
    LIST = 2  # cheeses from a list


@dataclass
class MazeConfig:
    """Describe the initialization strategy of a random maze"""

    # Maze Dimensions
    width: int = 21
    height: int = 15

    # Walls
    wall_density: float = 0.7
    symmetric: bool = True
    is_connected: bool = True

    # Mud
    mud_density: float = 0.1
    mud_range: int = 10

    # Cheeses
    # provide a list of cheese coordinates if you want a custom list of cheeses
    nb_cheese: int = 41
    cheese_mode: CheeseMode = CheeseMode.SYMMETRICAL
    cheeses: Optional[List[Coordinates]] = None  # This is ignored unless cheese_mode is CheeseMode.LIST

    def is_cheese_random(self) -> bool:
        return self.cheeses is None


class InitPlayerPosition(Enum):
    CORNER = 1  # Player positions are in the lower left and upper right corners
    SYMMETRIC = 2  # Player positions are random but symmetric
    ASYMMETRIC = 3  # Player positions are random (possibly assymetric)
    CUSTOM = 4  # Custom player positions.


@dataclass
class PlayerConfig:
    # Global
    symmetric: bool = True
    player_pos_init: InitPlayerPosition = InitPlayerPosition.CORNER

    # Player 1

    # This parameter is not considered if player_init_position is not InitPlayerPosition.CUSTOM
    # Give a tuple if you want to specify a custom position
    player1_pos: Optional[Coordinates] = None
    # Initial score
    player1_score: int = 0
    # Initial mud
    player1_mud: int = 0
    # Initial number of moves
    player1_moves: int = 0
    # Initial number of misses
    player1_misses: int = 0

    # Player 2

    # This parameter is not considered if player_init_position is not InitPlayerPosition.CUSTOM
    # Give a tuple if you want to specify a custom position
    player2_pos: Optional[Coordinates] = None
    # Initial score
    player2_score: int = 0
    # Initial mud
    player2_mud: int = 0
    # Initial number of moves
    player2_moves: int = 0
    # Initial number of misses
    player2_misses: int = 0

    def are_player_pos_symmetric(self):
        return self.player_pos_init == InitPlayerPosition.SYMMETRIC

    def are_player_pos_asymmetric(self) -> bool:
        return self.player_pos_init == InitPlayerPosition.ASYMMETRIC

    def are_player_pos_custom(self) -> bool:
        return (
                self.player_pos_init == InitPlayerPosition.CUSTOM
                and self.player1_pos is not None
                and self.player2_pos is not None
        )
