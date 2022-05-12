import pytest

from pyrat_engine.initializer.configs import MazeConfig, MudMode
from pyrat_engine.initializer.mud_generator import MudGenerator
from pyrat_engine.utils import central_symmetrical


@pytest.fixture
def config_random_symmetrical() -> MazeConfig:
    return MazeConfig(mud_mode=MudMode.RANDOM, symmetric=True)


@pytest.fixture
def config_random_asymmetrical() -> MazeConfig:
    return MazeConfig(mud_mode=MudMode.RANDOM, symmetric=False)


def test_symmetric(config_random_symmetrical: MazeConfig):
    """Test that the symmetric mode works well"""
    generator = MudGenerator(
        config_random_symmetrical.width, config_random_symmetrical.height
    )
    muds = generator.from_config({}, config_random_symmetrical)
    for coordinate, neighbors in muds.items():
        for neighbor in neighbors:
            # Mud in the range
            assert 0 < muds[coordinate][neighbor] <= config_random_symmetrical.mud_range
            # Other entry is there
            assert neighbor in muds and coordinate in muds[neighbor]
            assert muds[neighbor][coordinate] == muds[coordinate][neighbor]

            neighbor_symmetrical = central_symmetrical(
                neighbor,
                config_random_symmetrical.width,
                config_random_symmetrical.height,
            )
            coordinate_symmetrical = central_symmetrical(
                coordinate,
                config_random_symmetrical.width,
                config_random_symmetrical.height,
            )

            assert (
                neighbor_symmetrical in muds
                and coordinate_symmetrical in muds[neighbor_symmetrical]
            )
            assert (
                muds[neighbor_symmetrical][coordinate_symmetrical]
                == muds[neighbor][coordinate]
            )


def test_asymmetric(config_random_asymmetrical: MazeConfig):
    """Test that the asymmetric works well"""
    generator = MudGenerator(
        config_random_asymmetrical.width, config_random_asymmetrical.height
    )
    muds = generator.from_config({}, config_random_asymmetrical)
    for coordinate, neighbors in muds.items():
        for neighbor in neighbors:
            # Mud in the range
            assert (
                0 < muds[coordinate][neighbor] <= config_random_asymmetrical.mud_range
            )
            # Other entry is there
            assert neighbor in muds and coordinate in muds[neighbor]
            assert muds[neighbor][coordinate] == muds[coordinate][neighbor]
