from typing import List, Tuple

import copy

from pyrat_engine.engines.base import PyratEngine
from pyrat_engine.engines.numpy_vectorized.helpers import state_from_current_state
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Coordinates, Move


class NumpyEngine(PyratEngine):
    def __init__(self, state: CurrentGameState):
        self._original_state = state_from_current_state(state)
        self._current_state = state_from_current_state(state)

    def reset(self) -> None:
        self._current_state = copy.copy(self._original_state)

    def set_current_game_state(self, current_game_state: CurrentGameState) -> None:
        self._current_state = state_from_current_state(current_game_state)

    def get_current_game_state(self) -> CurrentGameState:
        pass

    def move(self, p1_move: Move, p2_move: Move) -> Tuple[float, float]:
        pass

    def unmove(
        self, p1_move: Move, p2_move: Move, cheeses: List[Coordinates] = None
    ) -> None:
        pass
