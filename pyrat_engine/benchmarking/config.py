from dataclasses import dataclass

from pyrat_engine.initializer.configs import MazeConfig, PlayerConfig


@dataclass
class BenchmarkConfig:
    nb_runs: int = 1000
    nb_moves_per_run: int = 200

    maze_config: MazeConfig = MazeConfig()
    player_config: PlayerConfig = PlayerConfig()
