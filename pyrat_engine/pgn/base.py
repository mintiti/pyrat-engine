from typing import List, Mapping, Tuple

from dataclasses import dataclass

from pyrat_engine.types import Coordinates, Move


@dataclass
class PGN:
    """PyRat Game Notation.
    Contains all the information needed to retrace the history of a game up to a given state"""

    # Initial state
    maze_width: int
    maze_height: int
    # Cheeses
    original_cheese_list: List[Coordinates]

    # Walls
    walls: List[Tuple[Coordinates, Coordinates]]

    # Mud
    mud: Mapping[Coordinates, Mapping[Coordinates, int]]

    # Player 1
    player1_pos: Coordinates
    # Initial score
    player1_score: int
    # Initial mud
    player1_mud: int
    # Initial number of moves
    player1_moves: int
    # Initial number of misses
    player1_misses: int

    # Player 2
    player2_pos: Coordinates
    # Initial score
    player2_score: int
    # Initial mud
    player2_mud: int
    # Initial number of moves
    player2_moves: int
    # Initial number of misses
    player2_misses: int

    # Action History
    player1_moves_history: List[Move]
    player2_moves_history: List[Move]

    @staticmethod
    def from_defaults(
        maze_width=21,
        maze_height=15,
        original_cheese_list=None,
        walls=None,
        mud=None,
        player1_pos=None,
        player1_score=0,
        player1_mud=0,
        player1_moves=0,
        player1_misses=0,
        player2_pos=None,
        player2_score=0,
        player2_mud=0,
        player2_moves=0,
        player2_misses=0,
        player1_moves_history=None,
        player2_moves_history=None,
    ) -> "PGN":

        # Handle defaults
        if original_cheese_list is None:
            original_cheese_list = []
        if walls is None:
            walls = []
        if mud is None:
            mud = {}
        if player1_pos is None:
            player1_pos = (0, 0)
        if player2_pos is None:
            player2_pos = (maze_width - 1, maze_height - 1)
        if player1_moves_history is None:
            player1_moves_history = []
        if player2_moves_history is None:
            player2_moves_history = []

        return PGN(
            maze_width=maze_width,
            maze_height=maze_height,
            original_cheese_list=original_cheese_list,
            walls=walls,
            mud=mud,
            player1_pos=player1_pos,
            player1_score=player1_score,
            player1_mud=player1_mud,
            player1_moves=player1_moves,
            player1_misses=player1_misses,
            player2_pos=player2_pos,
            player2_score=player2_score,
            player2_mud=player2_mud,
            player2_moves=player2_moves,
            player2_misses=player2_misses,
            player1_moves_history=player1_moves_history,
            player2_moves_history=player2_moves_history,
        )
