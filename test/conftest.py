import pytest
import random
from copy import deepcopy

from pyrat_engine.initializer.configs import MazeConfig
from pyrat_engine.initializer.initializer import CurrentStateInitializer
from pyrat_engine.state.base import CurrentGameState


@pytest.fixture
def small_maze_config() -> MazeConfig:
    return MazeConfig(width=5, height=5, nb_cheese=5, mud_density=0)


@pytest.fixture
def current_game_state(small_maze_config: MazeConfig) -> CurrentGameState:
    random.seed(4)
    return CurrentStateInitializer(maze_config=small_maze_config)()


@pytest.fixture
def current_game_state_with_mud(small_maze_config: MazeConfig) -> CurrentGameState:
    random.seed(2)
    maze_config = deepcopy(small_maze_config)
    maze_config.mud_density = 0.5
    return CurrentStateInitializer(maze_config=maze_config)()


@pytest.fixture
def current_game_state_with_mud_and_cheese(
    small_maze_config: MazeConfig,
) -> CurrentGameState:
    random.seed(18)
    maze_config = deepcopy(small_maze_config)
    maze_config.mud_density = 0.5
    return CurrentStateInitializer(maze_config=maze_config)()
