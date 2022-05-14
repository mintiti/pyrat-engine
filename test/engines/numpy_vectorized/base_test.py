import numpy as np
import pytest

from pyrat_engine.engines.numpy_vectorized.base import Board as NpBoard
from pyrat_engine.state.base import CurrentGameState


@pytest.fixture
def maze_2_2() -> CurrentGameState:
    """
    + ―― + ―― +
    | C  | S  |
    +    +    +
    | R  | C  |
    + ―― + ―― +"""
    return CurrentGameState(
        maze_width=2,
        maze_height=2,
        current_cheese_list=[(1, 0), (0, 1)],
        walls={(0, 0): [(1, 0)], (0, 1): [(1, 1)], (1, 0): [(0, 0)], (1, 1): [(0, 1)]},
        player1_pos=(0, 0),
        player2_pos=(1, 1),
    )


def test_board_init(maze_2_2):
    board = NpBoard(
        maze_width=maze_2_2.maze_width,
        maze_height=maze_2_2.maze_height,
        p1_pos=maze_2_2.player1_pos,
        p2_pos=maze_2_2.player2_pos,
        walls=maze_2_2.walls,
        muds=maze_2_2.mud,
        cheeses=maze_2_2.current_cheese_list,
    )
    # Player positions
    assert (
        board.player_positions
        == np.array([[[True, False], [False, False]], [[False, False], [False, True]]])
    ).all()
