import pytest
<<<<<<< HEAD
<<<<<<< HEAD

from pyrat_engine.engines.vanilla_py.player_move_handler import move
from pyrat_engine.render_utils.simple_printer.simple_printer import SimplePrinter
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Move


@pytest.fixture
def printer() -> SimplePrinter:
    return SimplePrinter()


class TestPlayerMoveHandler:
    def test_normal_moves(self, current_game_state: CurrentGameState):
        move(
            current_game_state=current_game_state, p1_move=Move.RIGHT, p2_move=Move.LEFT
        )
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2), (1, 3), (3, 1), (2, 0), (2, 4)],
            player1_pos=(1, 0),
            player1_score=0,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(3, 4),
            player2_score=0,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(
            current_game_state=current_game_state, p1_move=Move.RIGHT, p2_move=Move.LEFT
        )
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2), (1, 3), (3, 1)],
            player1_pos=(2, 0),
            player1_score=1,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(2, 4),
            player2_score=1,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(current_game_state=current_game_state, p1_move=Move.UP, p2_move=Move.DOWN)
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2), (1, 3), (3, 1)],
            player1_pos=(2, 1),
            player1_score=1,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(2, 3),
            player2_score=1,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(
            current_game_state=current_game_state, p1_move=Move.RIGHT, p2_move=Move.LEFT
        )
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2)],
            player1_pos=(3, 1),
            player1_score=2,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(1, 3),
            player2_score=2,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(current_game_state=current_game_state, p1_move=Move.UP, p2_move=Move.DOWN)
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2)],
            player1_pos=(3, 2),
            player1_score=2,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(1, 2),
            player2_score=2,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(
            current_game_state=current_game_state, p1_move=Move.LEFT, p2_move=Move.RIGHT
        )
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[],
            player1_pos=(2, 2),
            player1_score=2.5,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(2, 2),
            player2_score=2.5,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )

    def test_misses(self, current_game_state: CurrentGameState, printer: SimplePrinter):
        move(current_game_state=current_game_state, p1_move=Move.DOWN, p2_move=Move.UP)
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2), (1, 3), (3, 1), (2, 0), (2, 4)],
            player1_pos=(0, 0),
            player1_score=0,
            player1_misses=1,
            player1_mud=0,
            player2_pos=(4, 4),
            player2_score=0,
            player2_mud=0,
            player2_misses=1,
            walls=current_game_state.walls,
        )
=======
import random
=======
>>>>>>> move and maze

from pyrat_engine.engines.vanilla_py.player_move_handler import move
from pyrat_engine.render_utils.simple_printer.simple_printer import SimplePrinter
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Move


@pytest.fixture
def printer() -> SimplePrinter:
    return SimplePrinter()


class TestPlayerMoveHandler:
<<<<<<< HEAD
    def test_is_move_possible(self, current_game_state: CurrentGameState):
        print(current_game_state)
        assert 1 == 2
>>>>>>> finish move implementation
=======
    def test_normal_moves(self, current_game_state: CurrentGameState):
        move(
            current_game_state=current_game_state, p1_move=Move.RIGHT, p2_move=Move.LEFT
        )
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2), (1, 3), (3, 1), (2, 0), (2, 4)],
            player1_pos=(1, 0),
            player1_score=0,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(3, 4),
            player2_score=0,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(
            current_game_state=current_game_state, p1_move=Move.RIGHT, p2_move=Move.LEFT
        )
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2), (1, 3), (3, 1)],
            player1_pos=(2, 0),
            player1_score=1,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(2, 4),
            player2_score=1,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(current_game_state=current_game_state, p1_move=Move.UP, p2_move=Move.DOWN)
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2), (1, 3), (3, 1)],
            player1_pos=(2, 1),
            player1_score=1,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(2, 3),
            player2_score=1,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(
            current_game_state=current_game_state, p1_move=Move.RIGHT, p2_move=Move.LEFT
        )
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2)],
            player1_pos=(3, 1),
            player1_score=2,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(1, 3),
            player2_score=2,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(current_game_state=current_game_state, p1_move=Move.UP, p2_move=Move.DOWN)
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2)],
            player1_pos=(3, 2),
            player1_score=2,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(1, 2),
            player2_score=2,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )
        move(
            current_game_state=current_game_state, p1_move=Move.LEFT, p2_move=Move.RIGHT
        )
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[],
            player1_pos=(2, 2),
            player1_score=2.5,
            player1_misses=0,
            player1_mud=0,
            player2_pos=(2, 2),
            player2_score=2.5,
            player2_mud=0,
            player2_misses=0,
            walls=current_game_state.walls,
        )

    def test_misses(self, current_game_state: CurrentGameState, printer: SimplePrinter):
        move(current_game_state=current_game_state, p1_move=Move.DOWN, p2_move=Move.UP)
        assert current_game_state == CurrentGameState(
            maze_height=5,
            maze_width=5,
            current_cheese_list=[(2, 2), (1, 3), (3, 1), (2, 0), (2, 4)],
            player1_pos=(0, 0),
            player1_score=0,
            player1_misses=1,
            player1_mud=0,
            player2_pos=(4, 4),
            player2_score=0,
            player2_mud=0,
            player2_misses=1,
            walls=current_game_state.walls,
        )
>>>>>>> move and maze
