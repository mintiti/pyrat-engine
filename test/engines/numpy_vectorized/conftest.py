import pytest

from pyrat_engine.state.base import CurrentGameState


@pytest.fixture
def maze_3_2() -> CurrentGameState:
    """
    + ―― + ―― +
    | C  | S  |
    +    +    +
    | R  | C  |
    + ―― + ―― +"""
    return CurrentGameState(
        maze_width=3,
        maze_height=2,
        current_cheese_list=[(2, 0), (0, 1)],
        walls={(0, 0): [(1, 0)], (0, 1): [(1, 1)], (1, 0): [(0, 0)], (1, 1): [(0, 1)]},
        player1_pos=(0, 0),
        player2_pos=(2, 1),
    )


@pytest.fixture
def maze_2_2_mud() -> CurrentGameState:
    return CurrentGameState(
        maze_width=2,
        maze_height=2,
        current_cheese_list=[(1, 0), (0, 1)],
        mud={(0, 0): {(1, 0): 2, (0, 1): 2}, (0, 1): {(0, 0): 2}, (1, 0): {(0, 0): 2}},
        player1_pos=(0, 0),
        player2_pos=(1, 1),
    )
