import random
from typing import List, Optional, Set
from xmlrpc.client import Boolean
from pyrat_engine.init_configs import MazeConfig, PlayerConfig
from pyrat_engine.initializer.random_maze_state_generators import RandomMazeStateGenerators
from pyrat_engine.types import Coordinates



class Initializer:
    def __init__(self, player_config, maze_config, cheese_state):
        self.player_config = player_config
        self.maze_config = maze_config
        self.cheese_state = cheese_state 

    @staticmethod
    def fromConfiguration(player_config = PlayerConfig(), maze_config = MazeConfig()):
        initial_cheese_state = RandomMazeStateGenerators.generate_simple_random_cheese_state(maze_config) if maze_config.cheeses is None else maze_config.cheeses        
        return Initializer(player_config, maze_config, initial_cheese_state)
