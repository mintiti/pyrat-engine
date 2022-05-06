from typing import List

from pyrat_engine.engines.base import PyratEngine
from pyrat_engine.initializer.configs import MazeConfig, PlayerConfig
from pyrat_engine.initializer.initializer import CurrentStateInitializer
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Coordinates, Move


class VanillaPyEngine(PyratEngine):
    def __init__(
        self,
        player_config: PlayerConfig,
        maze_config: MazeConfig,
    ):
        self.initializer = CurrentStateInitializer(
            player_config=player_config,
            maze_config=maze_config,
        )
        self.initial_state: CurrentGameState = self.initializer()
        self.current_game_state: CurrentGameState = self.initializer()

    def initialize(self, game_state: CurrentGameState = None) -> None:
        """Changes the initial state of the board. This also sets the current game
        state to this initial state to keep them both referring to the same game
        instance. Call this if you want to start a new game."""
        if game_state is None:
            self.initial_state = self.initializer()
        else:
            self.initial_state = game_state
        self.current_game_state = self.initial_state

    def reset(self) -> None:
        """Reset the PGN to the initial state with the config provided."""
        self.set_current_game_state(self.initial_state)

    def set_current_game_state(self, current_game_state: CurrentGameState) -> None:
        """"""
        self.current_game_state = current_game_state

    def get_current_game_state(self) -> CurrentGameState:
        return self.current_game_state

    def move(self, p1_move: Move, p2_move: Move):
        return

    def unmove(self, p1_move: Move, p2_move: Move, cheeses: List[Coordinates] = None):
        return


class VanillaPyEngineBuilder:
    def __init__(self):
        self.player_config = None
        self.maze_config = None
        self.cheese_state = None

    def with_player_config(self, player_config: PlayerConfig):
        self.player_config = player_config

    def with_maze_config(self, maze_config: MazeConfig):
        self.maze_config = maze_config

    def build(self):
        return VanillaPyEngine(self.player_config, self.maze_config)
