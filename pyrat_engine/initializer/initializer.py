from pyrat_engine.initializer.configs import MazeConfig, PlayerConfig
from pyrat_engine.initializer.random_state_generators import (
    CheeseGenerator,
    PlayerPositionGenerator,
)
from pyrat_engine.state.base import CurrentGameState, HistoricGameState


class CurrentStateInitializer:
    """An initializer creates a CurrentGameState from initialization configurations"""

    def __init__(
        self,
        player_config: PlayerConfig = None,
        maze_config: MazeConfig = None,
    ):
        self.player_config = player_config if player_config else PlayerConfig()
        self.maze_config = maze_config if maze_config else MazeConfig()

    def __call__(self) -> CurrentGameState:
        p1_pos, p2_pos = PlayerPositionGenerator(
            maze_width=self.maze_config.width, maze_height=self.maze_config.height
        ).from_config(self.player_config)

        cheese_list = CheeseGenerator(p1_pos=p1_pos, p2_pos=p2_pos).from_maze_config(
            self.maze_config
        )
        # todo : init walls
        # todo : init mud
        return CurrentGameState.from_config(
            maze_config=self.maze_config,
            player_config=self.player_config,
            current_cheese_list=cheese_list,
        )


class HistoricStateInitializer:
    """An initializer creates a PGN from initialization configurations"""

    def __init__(
        self,
        player_config: PlayerConfig = None,
        maze_config: MazeConfig = None,
    ):
        self.player_config = player_config if player_config else PlayerConfig()
        self.maze_config = maze_config if maze_config else MazeConfig()

    def __call__(self) -> HistoricGameState:
        p1_pos, p2_pos = PlayerPositionGenerator(
            maze_width=self.maze_config.width, maze_height=self.maze_config.height
        ).from_config(self.player_config)
        cheese_list = CheeseGenerator(p1_pos=p1_pos, p2_pos=p2_pos).from_maze_config(
            self.maze_config
        )
        # todo : init walls
        # todo : init mud
        return HistoricGameState.from_config(
            maze_config=self.maze_config,
            player_config=self.player_config,
            current_cheese_list=cheese_list,
        )
