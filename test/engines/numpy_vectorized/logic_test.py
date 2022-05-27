import numpy as np
import numpy.typing as npt
import pytest

from pyrat_engine.engines.numpy_vectorized.helpers import state_from_current_state
from pyrat_engine.engines.numpy_vectorized.logic import (
    calculate_new_muds,
    compute_new_positions,
    move_down,
    move_left,
    move_right,
    move_up,
    update_cheese_and_score,
)
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Move


@pytest.fixture
def player_matrices() -> npt.NDArray[bool]:
    arr = np.zeros((2, 3, 3), dtype=bool)
    arr[0, 0, 0] = True
    arr[1, 2, 2] = True
    return arr


def test_move_up(player_matrices: npt.NDArray[bool]) -> None:
    ret = move_up(player_matrices[0])
    coordinate = ret.nonzero()
    # went from (0,0) to (0,1)
    assert coordinate[0] == 0
    assert coordinate[1] == 1

    ret = move_up(player_matrices[1])
    coordinate = ret.nonzero()
    # went from (2,2) to (2,0)
    assert coordinate[0] == 2
    assert coordinate[1] == 0


def test_move_down(player_matrices: npt.NDArray[bool]) -> None:
    ret = move_down(player_matrices[0])
    coordinate = ret.nonzero()
    # went from (0,0) to (0,2)
    assert coordinate[0] == 0
    assert coordinate[1] == 2

    ret = move_down(player_matrices[1])
    coordinate = ret.nonzero()
    # went from (2,2) to (2,1)
    assert coordinate[0] == 2
    assert coordinate[1] == 1


def test_move_right(player_matrices: npt.NDArray[bool]) -> None:
    ret = move_right(player_matrices[0])
    coordinate = ret.nonzero()
    # went from (0,0) to (1,0)
    assert coordinate[0] == 1
    assert coordinate[1] == 0

    ret = move_right(player_matrices[1])
    coordinate = ret.nonzero()
    # went from (2,2) to (0,2)
    assert coordinate[0] == 0
    assert coordinate[1] == 2


def test_move_left(player_matrices: npt.NDArray[bool]) -> None:
    ret = move_left(player_matrices[0])
    coordinate = ret.nonzero()
    # went from (0,0) to (2,0)
    assert coordinate[0] == 2
    assert coordinate[1] == 0

    ret = move_left(player_matrices[1])
    coordinate = ret.nonzero()
    # went from (2,2) to (1,2)
    assert coordinate[0] == 1
    assert coordinate[1] == 2


def test_compute_new_positions(maze_3_2: CurrentGameState):
    # Players are originally in (0,0) and (2,1)
    # There are walls between (0,0) and (1,0) and (0,1) and (1,1)
    state = state_from_current_state(maze_3_2)
    new_positions = compute_new_positions(state, p1_move=Move.UP, p2_move=Move.DOWN)
    player_positions = new_positions.nonzero()
    player_positions = np.stack(player_positions[:2]).T
    assert (player_positions[0] == [0, 1]).all()
    assert (player_positions[1] == [2, 0]).all()

    new_positions = compute_new_positions(state, p1_move=Move.DOWN, p2_move=Move.LEFT)
    player_positions = new_positions.nonzero()
    player_positions = np.stack(player_positions[:2]).T
    assert (player_positions[0] == [0, 0]).all()
    assert (player_positions[1] == [1, 1]).all()

    new_positions = compute_new_positions(
        state, p1_move=Move.DID_NOT_MOVE, p2_move=Move.RIGHT
    )
    player_positions = new_positions.nonzero()
    player_positions = np.stack(player_positions[:2]).T
    assert (player_positions[0] == [0, 0]).all()
    assert (player_positions[1] == [2, 1]).all()


def test_get_misses(maze_3_2: CurrentGameState):
    state = state_from_current_state(maze_3_2)

    def get_misses(
        player_positions: npt.NDArray[bool], new_positions: npt.NDArray[bool]
    ) -> npt.NDArray:
        return (state.board.player_positions == new_positions).all(axis=(0, 1))

    player_misses = get_misses(
        state.board.player_positions, state.board.player_positions
    )
    assert player_misses.size == 2
    assert (player_misses == [True, True]).all()

    new_positions = compute_new_positions(
        state, p1_move=Move.DID_NOT_MOVE, p2_move=Move.LEFT
    )
    player_misses = get_misses(state.board.player_positions, new_positions)
    assert (player_misses == [True, False]).all()

    new_positions = compute_new_positions(state, p1_move=Move.UP, p2_move=Move.RIGHT)
    player_misses = get_misses(state.board.player_positions, new_positions)
    assert (player_misses == [False, True]).all()


def test_get_muds(maze_2_2_mud: CurrentGameState):
    state = state_from_current_state(maze_2_2_mud)
    new_muds = calculate_new_muds(state, Move.UP, Move.RIGHT)
    assert (new_muds == [2, 1]).all()

    # test if the player is still stuck
    state.game_data.player_muds = np.array([3, 4])
    new_muds = calculate_new_muds(state, Move.UP, Move.RIGHT)
    assert (new_muds == [3, 4]).all()

    # test if only 1 of the players is still stuck
    state.game_data.player_muds = np.array([0, 4])
    new_muds = calculate_new_muds(state, Move.UP, Move.RIGHT)
    assert (new_muds == [2, 4]).all()

    # test if only 1 of the players is still stuck
    state.game_data.player_muds = np.array([4, 0])
    new_muds = calculate_new_muds(state, Move.UP, Move.RIGHT)
    assert (new_muds == [4, 1]).all()


def test_update_cheeses_and_scores(maze_2_2_mud: CurrentGameState):
    # Place the players on the cheeses
    maze_2_2_mud.player1_pos = (1, 0)
    maze_2_2_mud.player2_pos = (0, 1)
    state = state_from_current_state(maze_2_2_mud)
    update_cheese_and_score(state)
    assert (state.game_data.player_scores == [1, 1]).all()
    assert (state.board.cheeses == np.zeros((2, 2))).all()

    # Place 1 player on a cheese
    maze_2_2_mud.player1_pos = (1, 0)
    maze_2_2_mud.player2_pos = (1, 1)
    state = state_from_current_state(maze_2_2_mud)
    update_cheese_and_score(state)
    assert (state.game_data.player_scores == [1, 0]).all()
    cheese_board = np.zeros((2, 2), dtype=bool)
    cheese_board[0, 1] = True
    assert (state.board.cheeses == cheese_board).all()

    # Place 1 player on a cheese
    maze_2_2_mud.player1_pos = (0, 0)
    maze_2_2_mud.player2_pos = (0, 1)
    state = state_from_current_state(maze_2_2_mud)
    update_cheese_and_score(state)
    assert (state.game_data.player_scores == [0, 1]).all()
    cheese_board = np.zeros((2, 2), dtype=bool)
    cheese_board[1, 0] = True
    assert (state.board.cheeses == cheese_board).all()

    # players are on mud
    maze_2_2_mud.player1_pos = (1, 0)
    maze_2_2_mud.player2_pos = (0, 1)
    maze_2_2_mud.player1_mud = 10
    maze_2_2_mud.player2_mud = 10
    state = state_from_current_state(maze_2_2_mud)
    update_cheese_and_score(state)
    assert (state.game_data.player_scores == [0, 0]).all()
    cheese_board = np.zeros((2, 2), dtype=bool)
    cheese_board[0, 1] = True
    cheese_board[1, 0] = True
    assert (state.board.cheeses == cheese_board).all()

    # players are on mud
    maze_2_2_mud.player1_pos = (1, 0)
    maze_2_2_mud.player2_pos = (0, 1)
    maze_2_2_mud.player1_mud = 0
    maze_2_2_mud.player2_mud = 10
    state = state_from_current_state(maze_2_2_mud)
    update_cheese_and_score(state)
    assert (state.game_data.player_scores == [1, 0]).all()
    cheese_board = np.zeros((2, 2), dtype=bool)
    cheese_board[0, 1] = True
    assert (state.board.cheeses == cheese_board).all()

    # players are on mud
    maze_2_2_mud.player1_pos = (1, 0)
    maze_2_2_mud.player2_pos = (0, 1)
    maze_2_2_mud.player1_mud = 10
    maze_2_2_mud.player2_mud = 0
    state = state_from_current_state(maze_2_2_mud)
    update_cheese_and_score(state)
    assert (state.game_data.player_scores == [0, 1]).all()
    cheese_board = np.zeros((2, 2), dtype=bool)
    cheese_board[1, 0] = True
    assert (state.board.cheeses == cheese_board).all()
