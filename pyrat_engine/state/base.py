from typing import List, Mapping

from dataclasses import dataclass, field

from pyrat_engine.types import Coordinates, Move


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
<<<<<<< HEAD
    walls: Mapping[Coordinates, List[Coordinates]] = field(default_factory=dict)
=======
    walls: Mapping[Coordinates, List[Coordinates]]
>>>>>>> Add move handler

    # Mud
    mud: Mapping[Coordinates, Mapping[Coordinates, int]] = field(default_factory=dict)

    # Player 1
    player1_pos: Coordinates = (0, 0)
    # Current score
    player1_score: int = 0
    # Current mud
    player1_mud: int = 0
    # Current number of misses
    player1_misses: int = 0

    # Player 2
    player2_pos: Coordinates = (maze_width, maze_height)
    # Current score
    player2_score: int = 0
    # Current mud
    player2_mud: int = 0
    # Current number of misses
<<<<<<< HEAD
    player2_misses: int = 0
=======
    player2_misses: int

    @staticmethod
    def from_defaults(
        maze_config,
        player_config,
        current_cheese_list,
    ) -> "CurrentGameState":

        current_cheese_list = [] if current_cheese_list is None else current_cheese_list

        walls: Dict[Coordinates, List[Coordinates]] = (
            {} if maze_config.walls is None else maze_config.walls
        )

        mud: Dict[Coordinates, Dict[Coordinates, int]] = (
            {} if maze_config.mud is None else maze_config.mud
        )

        player1_pos = (
            (0, 0) if player_config.player1_pos is None else player_config.player1_pos
        )

        player2_pos = (
            (maze_config.maze_width - 1, maze_config.maze_height - 1)
            if player_config.player2_pos is None
            else player_config.player2_pos
        )

        return CurrentGameState(
            maze_width=maze_config.maze_width,
            maze_height=maze_config.maze_height,
            current_cheese_list=current_cheese_list,
            walls=walls,
            mud=mud,
            player1_pos=player1_pos,
            player1_score=player_config.player1_score,
            player1_mud=player_config.player1_mud,
            player1_misses=player_config.player1_misses,
            player2_pos=player2_pos,
            player2_score=player_config.player2_score,
            player2_mud=player_config.player2_mud,
            player2_misses=player_config.player2_misses,
        )
>>>>>>> Add move handler


@dataclass
class HistoricGameState:
    """Contains all the information needed to retrace the history of a game up to a
    certain point in time"""

    current_game_state: CurrentGameState = CurrentGameState()

    original_cheese_list: List[Coordinates] = field(default_factory=list)

    # Action History
<<<<<<< HEAD
    player1_moves_history: List[Move] = field(default_factory=list)
    player2_moves_history: List[Move] = field(default_factory=list)
=======
    player1_moves_history: List[Move]
    player2_moves_history: List[Move]

    @staticmethod
    def from_defaults(
        maze_config,
        player_config,
        current_cheese_list,
    ) -> "HistoricGameState":
        """Initializes the historic state from the start of the history"""

        current_cheese_list = [] if current_cheese_list is None else current_cheese_list

        walls: Dict[Coordinates, List[Coordinates]] = (
            {} if maze_config.walls is None else maze_config.walls
        )

        mud: Dict[Coordinates, Dict[Coordinates, int]] = (
            {} if maze_config.mud is None else maze_config.mud
        )

        player1_pos = (
            (0, 0) if player_config.player1_pos is None else player_config.player1_pos
        )

        player2_pos = (
            (maze_config.maze_width - 1, maze_config.maze_height - 1)
            if player_config.player2_pos is None
            else player_config.player2_pos
        )

        return HistoricGameState(
            current_game_state=CurrentGameState(
                maze_width=maze_config.maze_width,
                maze_height=maze_config.maze_height,
                current_cheese_list=current_cheese_list,
                walls=walls,
                mud=mud,
                player1_pos=player1_pos,
                player1_score=player_config.player1_score,
                player1_mud=player_config.player1_mud,
                player1_misses=player_config.player1_misses,
                player2_pos=player2_pos,
                player2_score=player_config.player2_score,
                player2_mud=player_config.player2_mud,
                player2_misses=player_config.player2_misses,
            ),
            original_cheese_list=current_cheese_list,
            player1_moves_history=[],
            player2_moves_history=[],
        )
>>>>>>> Add move handler
