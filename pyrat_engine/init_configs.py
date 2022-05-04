from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional, List

from pyrat_engine.types import Coordinates


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
    cheeses: Optional[List[Coordinates]] = None

    def is_cheese_random(self) -> bool:
        return self.cheeses is None

    @staticmethod
    def copy(width = width, height = height, wall_density = wall_density, symmetric = symmetric, is_connected = is_connected, mud_density = mud_density, mud_range = mud_range, cheeses = cheeses):
        return MazeConfig(width = width, height = height, wall_density = wall_density, symmetric = symmetric, is_connected = is_connected, mud_density = mud_density, mud_range = mud_range, cheeses = cheeses)

    


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
    player1_pos: Optional[Coordinates] = None  # Give a tuple if you want to specify a custom position
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
    player2_pos: Optional[Coordinates] = None  # Give a tuple if you want to specify a custom position
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
        return (self.player_pos_init == InitPlayerPosition.CUSTOM and
                self.player1_pos is not None and
                self.player2_pos is not None)

