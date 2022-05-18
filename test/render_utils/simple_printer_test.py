import pytest

from pyrat_engine.render_utils.simple_printer.simple_printer import (
    CurrentGameStateReader,
    SimplePrinter,
)
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
        maze_width=2,
        maze_height=2,
        current_cheese_list=[(1, 0), (0, 1)],
        walls={(0, 0): [(1, 0)], (0, 1): [(1, 1)], (1, 0): [(0, 0)], (1, 1): [(0, 1)]},
        player1_pos=(0, 0),
        player2_pos=(1, 1),
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


@pytest.fixture
def printer() -> SimplePrinter:
    return SimplePrinter()


def test_maze_string_normal(maze_2_2: CurrentGameState, printer: SimplePrinter):
    parser = CurrentGameStateReader(maze_2_2)
    ret = printer.make_maze(parser, maze_2_2)
    print(ret)
    assert (
        ret
        == """
     + ――― + ――― +
  1  |  C  |\x1b[1;32m  S  \x1b[0m|
     +     +     +
  0  |\x1b[1;31m  R  \x1b[0m|  C  |
     + ――― + ――― +
     +  0  +  1  """
    )


def test_maze_string_mud(maze_2_2_mud: CurrentGameState, printer: SimplePrinter):
    parser = CurrentGameStateReader(maze_2_2_mud)
    ret = printer.make_maze(parser, maze_2_2_mud)
    print(ret)
    assert (
        ret
        == """
     + ――― + ――― +
  1  |  C   \x1b[1;32m  S  \x1b[0m|
     + ┈┈┈ +     +
  0  |\x1b[1;31m  R  \x1b[0m┊  C  |
     + ――― + ――― +
     +  0  +  1  """
    )
