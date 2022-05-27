import numpy as np
import pytest

from pyrat_engine.engines.numpy_vectorized.base import Board as NpBoard
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.utils import get_direction, valid_neighbors


class TestBoard:
    @pytest.fixture
    def board_3_2(self, maze_3_2: CurrentGameState) -> NpBoard:
        return NpBoard(
            maze_width=maze_3_2.maze_width,
            maze_height=maze_3_2.maze_height,
            p1_pos=maze_3_2.player1_pos,
            p2_pos=maze_3_2.player2_pos,
            walls=maze_3_2.walls,
            muds=maze_3_2.mud,
            cheeses=maze_3_2.current_cheese_list,
        )

    def test_board__dimensions(
        self, board_3_2: NpBoard, maze_3_2: CurrentGameState
    ) -> None:
        # Maze dimensions
        assert (
            board_3_2.maze_width == maze_3_2.maze_width
            and board_3_2.maze_height == maze_3_2.maze_height
        )

    def test_board__player_positions(self, board_3_2: NpBoard) -> None:
        # Get the positions of the True values
        player_positions = board_3_2.player_positions.nonzero()
        # pack them into 3 dimensional coordinates
        player_positions = np.stack(player_positions).T
        # Rat (index 0) in position 0,0
        assert (player_positions[0] == [0, 0, 0]).all()
        # Snake (index 1) is in position 2,1
        assert (player_positions[1] == [2, 1, 1]).all()

    def test_board__walls(self, board_3_2: NpBoard, maze_3_2: CurrentGameState) -> None:
        # walls :
        for coordinate, neighbours in maze_3_2.walls.items():
            for neighbour in neighbours:
                move = get_direction(coordinate, neighbour)
                # can't move into the wall
                assert not board_3_2.can_move[coordinate][move]

    def test_board__muds(self, board_3_2: NpBoard, maze_3_2: CurrentGameState):  # noqa
        width = maze_3_2.maze_width
        height = maze_3_2.maze_height
        for i in range(width):
            for j in range(height):
                coordinate = (i, j)
                # There's no mud around the coordinate
                if coordinate not in maze_3_2.mud:
                    assert (board_3_2.cost[coordinate] == 1).all()
                    continue
                for neighbour in valid_neighbors(coordinate, width, height):
                    move = get_direction(coordinate, neighbour)
                    if neighbour in maze_3_2.mud[coordinate]:
                        assert (
                            maze_3_2.mud[coordinate][neighbour]
                            == board_3_2.cost[coordinate][move]
                        )
                    else:
                        assert board_3_2.cost[coordinate][move] == 1
