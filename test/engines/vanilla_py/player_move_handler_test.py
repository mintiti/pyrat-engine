import pytest
from copy import deepcopy

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

    def test_mud(
        self, current_game_state_with_mud: CurrentGameState, printer: SimplePrinter
    ):
        expected = deepcopy(current_game_state_with_mud)
        move(
            current_game_state=current_game_state_with_mud,
            p1_move=Move.RIGHT,
            p2_move=Move.LEFT,
        )
        expected.player1_pos = (1, 0)
        expected.player2_pos = (3, 4)
        expected.player1_mud = 2
        expected.player2_mud = 2
        expected.player1_misses = 0
        expected.player2_misses = 0
        assert current_game_state_with_mud == expected

        for _ in range(2):
            move(
                current_game_state=current_game_state_with_mud,
                p1_move=Move.RIGHT,
                p2_move=Move.LEFT,
            )
            expected.player1_mud -= 1
            expected.player2_mud -= 1
            expected.player1_misses += 1
            expected.player2_misses += 1
            assert current_game_state_with_mud == expected
        move(
            current_game_state=current_game_state_with_mud,
            p1_move=Move.RIGHT,
            p2_move=Move.LEFT,
        )
        expected.player1_pos = (2, 0)
        expected.player2_pos = (2, 4)
        assert current_game_state_with_mud == expected

    def test_mud_2(
        self,
        current_game_state_with_mud_and_cheese: CurrentGameState,
        printer: SimplePrinter,
    ):
        expected = deepcopy(current_game_state_with_mud_and_cheese)
        move(
            current_game_state=current_game_state_with_mud_and_cheese,
            p1_move=Move.UP,
            p2_move=Move.DOWN,
        )
        move(
            current_game_state=current_game_state_with_mud_and_cheese,
            p1_move=Move.RIGHT,
            p2_move=Move.LEFT,
        )
        expected.player1_pos = (1, 1)
        expected.player2_pos = (3, 3)
        expected.player1_mud = 10
        expected.player2_mud = 10

        for _ in range(9):
            move(
                current_game_state=current_game_state_with_mud_and_cheese,
                p1_move=Move.RIGHT,
                p2_move=Move.LEFT,
            )
            expected.player1_mud -= 1
            expected.player2_mud -= 1
            expected.player1_misses += 1
            expected.player2_misses += 1
            assert current_game_state_with_mud_and_cheese == expected

        move(
            current_game_state=current_game_state_with_mud_and_cheese,
            p1_move=Move.RIGHT,
            p2_move=Move.LEFT,
        )
        expected.player1_mud -= 1
        expected.player2_mud -= 1
        expected.player1_misses += 1
        expected.player2_misses += 1
        expected.player1_score += 1
        expected.player2_score += 1
        expected.current_cheese_list.remove((1, 1))
        expected.current_cheese_list.remove((3, 3))
        assert current_game_state_with_mud_and_cheese == expected

        move(
            current_game_state=current_game_state_with_mud_and_cheese,
            p1_move=Move.RIGHT,
            p2_move=Move.LEFT,
        )
        move(
            current_game_state=current_game_state_with_mud_and_cheese,
            p1_move=Move.UP,
            p2_move=Move.DOWN,
        )

        for _ in range(10):
            move(
                current_game_state=current_game_state_with_mud_and_cheese,
                p1_move=Move.RIGHT,
                p2_move=Move.LEFT,
            )

        printer.render(current_game_state_with_mud_and_cheese)

        expected.player1_pos = (2, 2)
        expected.player2_pos = (2, 2)
        expected.player1_mud = 0
        expected.player2_mud = 0
        expected.player1_misses = 20
        expected.player2_misses = 20
        expected.player1_score = 1.5
        expected.player2_score = 1.5
        expected.player1_mud = 0
        expected.player2_mud = 0
        expected.current_cheese_list.remove((2, 2))

        assert current_game_state_with_mud_and_cheese == expected
