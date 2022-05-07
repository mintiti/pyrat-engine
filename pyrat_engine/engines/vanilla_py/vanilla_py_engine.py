from typing import List, Optional, Tuple

from copy import deepcopy

from pyrat_engine.engines.base import PyratEngine
from pyrat_engine.initializer.configs import MazeConfig, PlayerConfig
from pyrat_engine.initializer.initializer import CurrentStateInitializer
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Coordinates, Move


class VanillaPyEngine(PyratEngine):
    def __init__(
        self,
        game_state: CurrentGameState,
    ):
        self.initial_state: CurrentGameState = game_state
        self.current_game_state: CurrentGameState = game_state

    def reset(self) -> None:
        """Reset the PGN to the initial state with the config provided."""
        self.set_current_game_state(self.initial_state)

    def set_current_game_state(self, current_game_state: CurrentGameState) -> None:
        """"""
        self.current_game_state = current_game_state

    def get_current_game_state(self) -> CurrentGameState:
        return deepcopy(self.current_game_state)

    def move(self, p1_move: Move, p2_move: Move) -> Tuple[float, float]:
        return (0.0, 0.0)  # placeholder for now

    def unmove(self, p1_move: Move, p2_move: Move, cheeses: List[Coordinates] = None):
        return


class VanillaPyEngineConfigBuilder:
    def __init__(self):
        self.player_config: Optional[PlayerConfig] = None
        self.maze_config: Optional[MazeConfig] = None

    def with_player_config(self, player_config: PlayerConfig):
        self.player_config = player_config

    def with_maze_config(self, maze_config: MazeConfig):
        self.maze_config = maze_config

    def build(self):
        return VanillaPyEngine(
            CurrentStateInitializer(
                player_config=self.player_config,
                maze_config=self.maze_config,
            )()
        )
