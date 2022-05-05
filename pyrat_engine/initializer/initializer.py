from pyrat_engine.init_configs import MazeConfig, PlayerConfig
from pyrat_engine.initializer.random_maze_state_generators import (
    CheeseGenerator,
    PlayerPositionGenerator
)
from pyrat_engine.pgn import PGN


class Initializer:
    """An initializer creates a PGN from initialization configurations"""

    def __init__(self, player_config: PlayerConfig = PlayerConfig(),
                 maze_config: MazeConfig = MazeConfig()):
        self.player_config = player_config
        self.maze_config = maze_config

    def __call__(self) -> PGN:
        player_pos_initializer = PlayerPositionGenerator(maze_width=self.maze_config.width,
                                                         maze_height=self.maze_config.height)
        p1_pos, p2_pos = player_pos_initializer.from_config(self.player_config)
        cheese_list = CheeseGenerator(p1_pos=p1_pos, p2_pos=p2_pos).from_maze_config(self.maze_config)
        # todo : init walls
        # todo : init mud
        return PGN()
