import random
from typing import List, Optional, Set
from xmlrpc.client import Boolean
from pyrat_engine.init_configs import MazeConfig, PlayerConfig
from pyrat_engine.types import Coordinates



class Initializer:
    def __init__(self, player_config, maze_config, cheese_state):
        self.player_config = player_config
        self.maze_config = maze_config
        self.cheese_state = cheese_state
        pass 


    ### refactor in a generator class??
    @staticmethod
    def _simple_random_cheese_state_generator(maze_config: MazeConfig):
        cheese_number = 15
        previous_cheeses_positions = set()
        previous_cheeses_positions.add((maze_config.width // 2, maze_config.height // 2))
        yield (maze_config.width // 2, maze_config.height // 2)
        for i in range(0, cheese_number // 2):
            cheese_x = random.randint(0, maze_config.width)
            cheese_y = random.randint(0, maze_config.height)
            while (cheese_x, cheese_y) in previous_cheeses_positions:
                cheese_x = random.randint(0, maze_config.width)
                cheese_y = random.randint(0, maze_config.height)
            
            # Add cheese to the previous ones and yield it
            previous_cheeses_positions.add((cheese_x, cheese_y))
            yield (cheese_x, cheese_y)

            # Add the symmetric to the previous ones and yield it
            previous_cheeses_positions.add((maze_config.width - cheese_x, maze_config.height - cheese_y))
            yield (maze_config.width - cheese_x, maze_config.height - cheese_y)


    @staticmethod
    def generate_simple_random_cheese_state(maze_config: MazeConfig) -> MazeConfig:
        return MazeConfig.copy(cheeses=[cheese_position for cheese_position in Initializer._simple_random_cheese_state_generator(maze_config)])
    

    @staticmethod
    def fromConfiguration(player_config = PlayerConfig(), maze_config = MazeConfig()):
        initial_cheese_state = Initializer.generate_simple_random_cheese_state(maze_config) if maze_config.cheeses is None else maze_config.cheeses        
        return Initializer(player_config, maze_config, initial_cheese_state)
