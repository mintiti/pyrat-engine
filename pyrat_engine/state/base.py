from typing import List

from dataclasses import dataclass, field

from pyrat_engine.types import Coordinates, Move, Muds, Walls


@dataclass
class CurrentGameState:
    """Contains all the information needed to define a game state at a certain point in
    time"""

    # Current state
    maze_width: int = 21
    maze_height: int = 15

    # Cheeses
    current_cheese_list: List[Coordinates] = field(default_factory=list)

    # Walls
    walls: Walls = field(default_factory=dict)

    # Mud
    mud: Muds = field(default_factory=dict)

    # Player 1
    player1_pos: Coordinates = (0, 0)
    # Current score
    player1_score: float = 0
    # Current mud
    player1_mud: int = 0
    # Current number of misses
    player1_misses: int = 0

    # Player 2
    player2_pos: Coordinates = (maze_width - 1, maze_height - 1)
    # Current score
    player2_score: float = 0
    # Current mud
    player2_mud: int = 0
    # Current number of misses
    player2_misses: int = 0


@dataclass
class HistoricGameState:
    """Contains all the information needed to retrace the history of a game up to a
    certain point in time"""

    current_game_state: CurrentGameState = CurrentGameState()

    original_cheese_list: List[Coordinates] = field(default_factory=list)

    # Action History
    player1_moves_history: List[Move] = field(default_factory=list)
    player2_moves_history: List[Move] = field(default_factory=list)
