from abc import ABC, abstractmethod
from typing import List, Tuple

from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Coordinates, Move


class PyratEngine(ABC):
    """Interface definition for a PyratEngine.
    The engine is purely responsible for setting a (deterministic) state and running
    it"""

    @abstractmethod
    def reset(self) -> None:
        """Reset the game according to the initialization parameters"""

    @abstractmethod
    def set_current_game_state(self, current_game_state: CurrentGameState) -> None:
        """
        Set the state of the game to the given current_game_state
        Args:
            current_game_state: the state of the game to set
        """

    @abstractmethod
    def get_current_game_state(self) -> CurrentGameState:
        """Get the CurrentGameState representation of the current state
        Returns:
            A CurrentGameState representation of the current game state
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
    def unmove(
        self, p1_move: Move, p2_move: Move, cheeses: List[Coordinates] = None
    ) -> None:
        """Unmake the moves for each player, then put the cheeses back in.
        Args:
            p1_move: the move to unmake for player 1
            p2_move: the move to unmake for player 2
            cheeses: (optional) Any cheeses to put back in
        """
