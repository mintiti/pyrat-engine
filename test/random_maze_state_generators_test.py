import random

from pyrat_engine.initializer.configs import MazeConfig
from pyrat_engine.initializer.random_state_generators import CheeseGenerator


def test_generate_random_cheese_list():
    random.seed(1)
    expected_list = [
        (10, 7),
        (4, 2),
        (17, 13),
        (8, 3),
        (13, 12),
        (15, 14),
        (6, 1),
        (15, 12),
        (6, 3),
        (15, 0),
        (6, 15),
        (12, 13),
        (9, 2),
        (19, 0),
        (2, 15),
    ]
    assert (
        CheeseGenerator.generate_simple_random_cheese_state(
            maze_config=MazeConfig()
        ).cheeses
        == expected_list
    )
