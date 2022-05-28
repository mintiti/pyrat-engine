from typing import Callable

import random

from pyrat_engine.engines.base import PyratEngine
from pyrat_engine.initializer.configs import MazeConfig, PlayerConfig
from pyrat_engine.initializer.initializer import CurrentStateInitializer
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Move


def profile_move(
    engine_cls: Callable[[CurrentGameState], PyratEngine],
    nb_moves: int,
    maze_config: MazeConfig = None,
    player_config: PlayerConfig = None,
):
    # Default parameters if not specified
    if maze_config is None:
        maze_config = MazeConfig()
    if player_config is None:
        player_config = PlayerConfig()

    state_initializer = CurrentStateInitializer(
        player_config=player_config, maze_config=maze_config
    )
    state = state_initializer()
    engine = engine_cls(state)
    list_moves = list(Move)
    for _ in range(nb_moves):
        p1_move: Move = random.choice(list_moves)
        p2_move: Move = random.choice(list_moves)
        engine.move(p1_move, p2_move)
