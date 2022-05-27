import numpy as np
import numpy.typing as npt

from pyrat_engine.engines.numpy_vectorized.base import Board, NumpyState
from pyrat_engine.types import Move


def move_up(player_position_matrix: npt.NDArray):
    """
    move a player up whether it is possible or not
    Args:
        player_position_matrix: The player position matrix to move the player on

    Returns:
        the new board
    """
    return np.roll(player_position_matrix, shift=1, axis=1)


def move_down(player_position_matrix: npt.NDArray):
    """
    move a player down whether it is possible or not
    Args:
        player_position_matrix: The player position matrix to move the player on

    Returns:
        the new board
    """
    return np.roll(player_position_matrix, shift=-1, axis=1)


def move_right(player_position_matrix: npt.NDArray):
    """
    move a player right whether it is possible or not
    Args:
        player_position_matrix: The player position matrix to move the player on

    Returns:
        the new board
    """
    return np.roll(player_position_matrix, shift=1, axis=0)


def move_left(player_position_matrix: npt.NDArray):
    """
    move a player left whether it is possible or not
    Args:
        player_position_matrix: The player position matrix to move the player on

    Returns:
        the new board
    """
    return np.roll(player_position_matrix, shift=-1, axis=0)


def move_player(player_position_matrix: npt.NDArray, player_move: Move):
    """Handle moving one player"""
    if player_move == Move.DID_NOT_MOVE:
        return player_position_matrix.copy()
    if player_move == Move.UP:
        return move_up(player_position_matrix)
    elif player_move == Move.RIGHT:
        return move_right(player_position_matrix)
    elif player_move == Move.LEFT:
        return move_left(player_position_matrix)
    else:
        return move_down(player_position_matrix)


def move_players(board: Board, player1_move: Move, player2_move: Move):
    """
    Move the players without checking move correctness
    Args:
        board:
        player1_move: The move for player 1
        player2_move: The move for player 2

    Returns:
        The new board with moved players
    """
    new_board = np.empty_like(board.player_positions, dtype=bool)
    new_board[..., 0] = move_player(board.player_positions[..., 0], player1_move)
    new_board[..., 1] = move_player(board.player_positions[..., 1], player2_move)

    return new_board


def end_turn(state: NumpyState):
    """End the turn chores"""
    state.game_data.player_muds -= 1


def calculate_new_muds(state: NumpyState, p1_move: Move, p2_move: Move):
    """
    Calculate the new player muds after they move from their position.
    Does not change it if the player is still in a previous mud
    Args:
        state: The current NumpyState
        p1_move: player 1's move
        p2_move: player 2's move

    Returns:
        a (2,) array containing each player's mud
    """
    is_stuck = state.game_data.player_muds > 0
    move_cost = np.ones((2,), dtype=int)
    move_cost[0] = state.board.cost[state.board.player_positions[..., 0]][0][p1_move]
    move_cost[1] = state.board.cost[state.board.player_positions[..., 1]][0][p2_move]

    new_muds = (
        is_stuck * state.game_data.player_muds + np.logical_not(is_stuck) * move_cost
    )

    return new_muds


def update_cheese_and_score(state: NumpyState):
    # Player gets points if he actually got to the cheese
    should_get_points = state.game_data.player_muds <= 0
    # (2,maze_width,maze_height)
    taken_cheeses = should_get_points * np.logical_and(
        state.board.cheeses[..., np.newaxis], state.board.player_positions
    )
    # (maze_width,maze_height)
    player_per_cell = state.board.player_positions.sum(axis=2)
    # (2,)
    points = np.nan_to_num(
        taken_cheeses / player_per_cell[..., np.newaxis], copy=False
    ).sum(axis=(0, 1))

    # (maze_width, maze_height)
    new_cheeses = np.logical_xor(state.board.cheeses, taken_cheeses.sum(axis=2))

    # update scores
    state.game_data.player_scores += points
    # update cheeses
    state.board.cheeses = new_cheeses


def move(state: NumpyState, p1_move: Move, p2_move: Move):
    # Calculate the player positions
    new_player_pos = compute_new_positions(state, p1_move, p2_move)

    # Player has missed if his position is the same as before
    player_misses = (state.board.player_positions == new_player_pos).all(axis=(0, 1))
    # Update misses
    state.game_data.player_misses += player_misses

    # Update the player positions
    state.board.player_positions = new_player_pos
    # Calculate the new muds
    new_muds = calculate_new_muds(state, p1_move, p2_move)
    state.game_data.player_muds = new_muds
    # decrement the muds because the player moved now
    state.game_data.player_muds -= 1
    update_cheese_and_score(state)


def compute_new_positions(
    state: NumpyState, p1_move: Move, p2_move: Move
) -> npt.NDArray:
    """
    Calculate the new player positions, taking into account walls, labyrinth boundaries
    and player's current mud status
    Args:
        state: the current NumpyState
        p1_move: player 1's move
        p2_move: player 2's move

    Returns:
        The updated player position matrix
    """
    # Players are stuck because of previous mud
    is_stuck = state.game_data.player_muds > 0  # (2,) array
    # The move chosen makes the player move
    can_move = np.zeros((2,), dtype=bool)
    can_move[0] = state.board.can_move[state.board.player_positions[..., 0]][0][p1_move]
    can_move[1] = state.board.can_move[state.board.player_positions[..., 1]][0][p2_move]
    should_stay_in_place = is_stuck | np.logical_not(can_move)
    # We use Transpose here because we want broadcasting from the left (player planes)
    # Numpy broadcasts from the right
    new_player_pos = (
        should_stay_in_place * state.board.player_positions
        + np.logical_not(should_stay_in_place)
        * move_players(state.board, player1_move=p1_move, player2_move=p2_move)
    )

    return new_player_pos
