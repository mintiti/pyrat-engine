from copy import deepcopy

from pyrat_engine.initializer.configs import MazeConfig, PlayerConfig
from pyrat_engine.initializer.mud_generator import MudGenerator
from pyrat_engine.initializer.random_state_generators import (
    CheeseGenerator,
    PlayerPositionGenerator,
    WallsGenerator,
)
from pyrat_engine.state.base import CurrentGameState, HistoricGameState


class CurrentStateInitializer:
    """An initializer creates a CurrentGameState from initialization configurations"""

    def __init__(
        self,
        player_config: PlayerConfig = None,
        maze_config: MazeConfig = None,
    ):
        self.player_config = (
            player_config if player_config is not None else PlayerConfig()
        )
        self.maze_config = maze_config if maze_config is not None else MazeConfig()

    def __call__(self) -> CurrentGameState:
        p1_pos, p2_pos = PlayerPositionGenerator(
            maze_width=self.maze_config.width, maze_height=self.maze_config.height
        ).from_config(self.player_config)
        cheese_list = CheeseGenerator(p1_pos=p1_pos, p2_pos=p2_pos).from_maze_config(
            self.maze_config
        )
        walls = WallsGenerator().from_maze_config(self.maze_config)

        mud = MudGenerator().from_maze_config_and_walls(
            maze_config=self.maze_config, walls=walls
        )

        return CurrentGameState(
            maze_width=self.maze_config.width,
            maze_height=self.maze_config.height,
            player1_pos=p1_pos,
            player2_pos=p2_pos,
            current_cheese_list=cheese_list,
            walls=walls,
            mud=mud,
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
        current_game_state = CurrentStateInitializer(
            maze_config=self.maze_config, player_config=self.player_config
        )()

        return HistoricGameState(
            current_game_state=current_game_state,
            original_cheese_list=deepcopy(current_game_state.current_cheese_list),
            player1_moves_history=[],
            player2_moves_history=[],
        )
