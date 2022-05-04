### refactor in a generator class??
import random
from pyrat_engine.init_configs import MazeConfig


class RandomMazeStateGenerators:
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
        return MazeConfig.copy(cheeses=[cheese_position for cheese_position in RandomMazeStateGenerators._simple_random_cheese_state_generator(maze_config)])