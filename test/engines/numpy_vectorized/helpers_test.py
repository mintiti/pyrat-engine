from pyrat_engine.engines.numpy_vectorized.helpers import (
    board_from_current_game_state,
    get_current_cheese_list,
    get_muds,
    get_player_positions,
    get_walls,
)
from pyrat_engine.state.base import CurrentGameState


def test_get_player_positions(maze_3_2: CurrentGameState):
    board = board_from_current_game_state(maze_3_2)
    player_positions = get_player_positions(board)
    assert (player_positions[0] == [0, 0]).all()
    assert (player_positions[1] == [2, 1]).all()


def test_get_muds(maze_2_2_mud: CurrentGameState):
    board = board_from_current_game_state(maze_2_2_mud)
    mud = get_muds(board)
    assert mud == {
        (0, 0): {(0, 1): 2, (1, 0): 2},
        (0, 1): {(0, 0): 2},
        (1, 0): {(0, 0): 2},
    }


def test_get_walls(maze_3_2: CurrentGameState):
    board = board_from_current_game_state(maze_3_2)
    walls = get_walls(board)
    for coordinate in walls:
        for neighbor in walls[coordinate]:
            assert neighbor in maze_3_2.walls[coordinate]

    for coordinate in maze_3_2.walls:
        for neighbor in maze_3_2.walls[coordinate]:
            assert neighbor in walls[coordinate]


def test_get_cheese_list(maze_3_2: CurrentGameState):
    board = board_from_current_game_state(maze_3_2)
    cheeses = get_current_cheese_list(board)
    assert len(cheeses) == len(maze_3_2.current_cheese_list)
    for cheese in cheeses:
        assert cheese in maze_3_2.current_cheese_list


def test_board_from_game_state(maze_3_2: CurrentGameState):
    board = board_from_current_game_state(maze_3_2)
    assert board.maze_height == maze_3_2.maze_height
    assert board.maze_width == maze_3_2.maze_width
