from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, List

from pyrat_engine.init_configs import MazeConfig, PlayerConfig
from pyrat_engine.pgn import PGN
from pyrat_engine.types import Coordinates


class Move(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


class PyratEngine(ABC):
    """Interface definition for a PyratEngin"""

    @abstractmethod
    def initialize(
        self,
        maze_config: MazeConfig = None,
        player_config: PlayerConfig = None,
        pgn: PGN = None,
    ):
        """Reads the initialization configuration and PGN and initializes the board"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the game according to the initialization parameters"""
        pass

    @abstractmethod
    def set_pgn(self, pgn: PGN) -> None:
        """
        Set the state of the game to the given pgn
        Args:
            pgn: the state of the game to set
        """

    @abstractmethod
    def get_pgn(self) -> PGN:
        """Get the PGN representation of the current state
        Returns:
            A PGN representation of the current game state
        """

    @abstractmethod
    def move(self, p1_move: Move, p2_move: Move) -> Tuple[float, float]:
        """Make the player moves on the current board
        Args:
            p1_move: The move from player 1
            p2_move: The move from player 2

        Returns:
            The number of points gained by each players
        """

    @abstractmethod
    def unmove(self, p1_move: Move, p2_move: Move, cheeses: List[Coordinates] = None):
        """Unmake the moves for each players, then put the cheeses back in.
        Args:
            p1_move: the move to unmake for player 1
            p2_move: the move to unmake for player 2
            cheeses: (optional) Any cheeses to put back in
        """
