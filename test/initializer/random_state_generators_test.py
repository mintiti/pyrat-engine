import pytest

from pyrat_engine.initializer.configs import MazeConfig
from pyrat_engine.initializer.random_state_generators import (
    PlayerPositionGenerator,
    WallsGenerator,
)


@pytest.fixture
def player_position_generator() -> PlayerPositionGenerator:
    return PlayerPositionGenerator(21, 15)


class TestPlayerPositionGenerator:
    def test_corner_positions(self, player_position_generator: PlayerPositionGenerator):
        """Test the corner position generator"""
        p1_pos, p2_pos = player_position_generator._corner_positions()
        # Players are in bounds
        assert p1_pos[0] < 21
        assert p1_pos[1] < 15

        assert p2_pos[0] < 21
        assert p2_pos[1] < 15

        # Players are in the corners
        assert p1_pos == (0, 0)
        assert p2_pos == (20, 14)

    def test_symmetric(self, player_position_generator: PlayerPositionGenerator):
        """Test symmetric initialization"""
        for _ in range(100):
            p1_pos, p2_pos = player_position_generator._symmetric()

            # Players are in bounds
            assert p1_pos[0] < 21
            assert p1_pos[1] < 15

            assert p2_pos[0] < 21
            assert p2_pos[1] < 15
            p1_symmetric = (21 - p1_pos[0] - 1, 15 - p1_pos[1] - 1)
            assert p1_symmetric == p2_pos

    def test_asymmetric(self, player_position_generator: PlayerPositionGenerator):
        """Test symmetric initialization"""
        for _ in range(100):
            p1_pos, p2_pos = player_position_generator._asymmetric()

            # Players are in bounds
            assert p1_pos[0] < 21
            assert p1_pos[1] < 15

            assert p2_pos[0] < 21
            assert p2_pos[1] < 15


class TestWallsGenerator:
    def test_wall_generator_symmetric(self, small_maze_config: MazeConfig):
        walls = WallsGenerator().from_maze_config(small_maze_config)
        assert walls == {
            (0, 0): [(1, 0)],
            (0, 1): [(0, 2)],
            (0, 2): [(0, 1)],
            (0, 3): [(1, 3)],
            (0, 4): [],
            (1, 0): [(0, 0)],
            (1, 1): [],
            (1, 2): [],
            (1, 3): [(2, 3), (0, 3)],
            (1, 4): [],
            (2, 0): [],
            (2, 1): [(2, 2), (3, 1)],
            (2, 2): [(2, 3), (2, 1)],
            (2, 3): [(2, 2), (1, 3)],
            (2, 4): [],
            (3, 0): [],
            (3, 1): [(4, 1), (2, 1)],
            (3, 2): [],
            (3, 3): [],
            (3, 4): [(4, 4)],
            (4, 0): [],
            (4, 1): [(3, 1)],
            (4, 2): [(4, 3)],
            (4, 3): [(4, 2)],
            (4, 4): [(3, 4)],
        }
