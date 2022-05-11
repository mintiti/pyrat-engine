import pytest
import random

from pyrat_engine.initializer.initializer import CurrentStateInitializer
from pyrat_engine.state.base import CurrentGameState


@pytest.fixture
def current_game_state() -> CurrentGameState:
    random.seed(1)
    return CurrentStateInitializer()()


class TestPlayerMoveHandler:
    def test_is_move_possible(self, current_game_state: CurrentGameState):
        print(current_game_state)
        assert 1 == 2
