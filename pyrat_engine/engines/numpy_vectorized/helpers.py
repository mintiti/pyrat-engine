import typing
from typing import List

import numpy as np
import numpy.typing as npt

from pyrat_engine.engines.numpy_vectorized.base import Board, GameData, NumpyState
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Coordinates, Muds, Walls
from pyrat_engine.utils import add_mud, add_wall, get_direction, valid_neighbors


def board_from_current_game_state(state: CurrentGameState) -> Board:
    return Board(
        maze_width=state.maze_width,
        maze_height=state.maze_height,
        p1_pos=state.player1_pos,
        p2_pos=state.player2_pos,
        walls=state.walls,
        muds=state.mud,
        cheeses=state.current_cheese_list,
    )


def game_data_from_current_game_state(state: CurrentGameState) -> GameData:
    return GameData(
        player_scores=np.array(
            [state.player1_score, state.player2_score], dtype=np.float16
        ),
        player_muds=np.array([state.player1_mud, state.player2_mud], dtype=int),
        player_misses=np.array([state.player1_misses, state.player2_misses], dtype=int),
    )


def state_from_current_state(current_game_state: CurrentGameState) -> NumpyState:
    return NumpyState(
        board=board_from_current_game_state(current_game_state),
        game_data=game_data_from_current_game_state(current_game_state),
    )


def get_current_cheese_list(board: Board) -> List[Coordinates]:
    """Return the list of cheeses from the Board, in lexicographical order"""
    cheeses_positions = board.cheeses.nonzero()
    cheeses_positions = np.stack(cheeses_positions).T
    cheeses: List[Coordinates] = list(
        map(lambda x: typing.cast(Coordinates, tuple(x)), cheeses_positions)
    )
    cheeses.sort()
    return cheeses


def get_walls(board: Board) -> Walls:
    walls: Walls = {}
    for i in range(board.maze_width):
        for j in range(board.maze_height):
            coordinate = (i, j)
            for neighbour in valid_neighbors(
                coordinate, board.maze_width, board.maze_height
            ):
                move = get_direction(coordinate, neighbour)
                if not board.can_move[coordinate][move]:
                    wall = (coordinate, neighbour)
                    add_wall(walls, wall)
    return walls


def get_muds(board: Board) -> Muds:
    muds: Muds = {}
    for i in range(board.maze_width):
        for j in range(board.maze_height):
            coordinate = (i, j)
            for neighbor in valid_neighbors(
                coordinate, board.maze_width, board.maze_height
            ):
                move = get_direction(coordinate, neighbor)
                cost = board.cost[coordinate][move]
                if cost > 1:
                    add_mud(muds, coordinate, neighbor, cost)
    return muds


def get_player_positions(board) -> npt.NDArray[int]:
    """
    Return a (nb_player,2) array containing player positions
    Args:
        board: the board to extract the information from

    Returns:
        an array where :
            array[0] are the coordinates of the first player
            array[1] are the coordinates of the second player
    """
    # Get the positions of the True values
    player_positions = board.player_positions.nonzero()
    # pack them into 3 dimensional coordinates
    player_positions = np.stack(player_positions[1:]).T
    return player_positions


def current_game_state_from_state(state: NumpyState) -> CurrentGameState:
    board = state.board
    game_data = state.game_data
    player_positions: npt.NDArray[int] = get_player_positions(board)
    return CurrentGameState(
        maze_width=board.maze_width,
        maze_height=board.maze_height,
        current_cheese_list=get_current_cheese_list(board),
        walls=get_walls(board),
        mud=get_muds(board),
        player1_pos=typing.cast(Coordinates, tuple(player_positions[0])),
        player1_score=game_data.player_scores[0],
        player1_mud=game_data.player_muds[0],
        player1_misses=game_data.player_misses[0],
        player2_pos=typing.cast(Coordinates, tuple(player_positions[1])),
        player2_score=game_data.player_scores[1],
        player2_mud=game_data.player_muds[1],
        player2_misses=game_data.player_misses[1],
    )
