from typing import Dict, List, Set, Tuple

import random
from itertools import product

from pyrat_engine.initializer.configs import MazeConfig, MudMode
from pyrat_engine.types import Coordinates, Mud
from pyrat_engine.utils import (
    add_mud,
    central_symmetrical,
    order_node_pair,
    valid_neighbors,
)


def _is_wall_present(
    coordinate: Coordinates,
    other: Coordinates,
    walls: Dict[Coordinates, List[Coordinates]],
):
    """Tells us whether theres a wall between coordinate and other"""
    return (coordinate in walls and other in walls[coordinate]) or (
        other in walls and coordinate in walls[other]
    )


class MudGenerator:
    def from_maze_config_and_walls(
        self, maze_config: MazeConfig, walls: Dict[Coordinates, List[Coordinates]]
    ) -> Dict[Coordinates, Dict[Coordinates, int]]:
        """
        Dispatch creating the mud configuration from a maze configuration
        Args:
            walls: Walls that are already in the maze
            maze_config: The maze_config to parse

        Returns:
            A mud Dict
        """
        if maze_config.mud_mode == MudMode.RANDOM:
            return self._generate_mud(
                maze_config, walls, is_symmetric=maze_config.symmetric
            )
        else:
            assert (
                maze_config.mud is not None
            ), "mud_mode is MudMode.RANDOM, but not mud was provided."
            return maze_config.mud

    def _generate_mud(
        self,
        maze_config: MazeConfig,
        walls: Dict[Coordinates, List[Coordinates]],
        is_symmetric: bool,
    ) -> Dict[Coordinates, Dict[Coordinates, int]]:
        """
        Return a symmetric mud configuration.
        Returns:
            The Dict of mud
        """
        possible_muds = self._possible_muds(maze_config, walls)
        muds: Dict[Coordinates, Dict[Coordinates, int]] = {}
        number_of_muds = 0
        random.shuffle(possible_muds)
        visited_muds: Set[Mud] = set()

        for mud in possible_muds:
            if number_of_muds / len(possible_muds) >= maze_config.mud_density:
                break
            node, other_node = mud
            if order_node_pair(node, other_node) in visited_muds:
                continue
            value = self._get_mud_value(maze_config.mud_range)
            add_mud(muds, node, other_node, value)
            visited_muds.add(order_node_pair(node, other_node))
            number_of_muds += 1

            if not is_symmetric:
                continue
            # Add the symmetrical mud
            symmetric_0 = central_symmetrical(
                mud[0], maze_config.width, maze_config.height
            )
            symmetric_1 = central_symmetrical(
                mud[1], maze_config.width, maze_config.height
            )
            add_mud(muds, symmetric_0, symmetric_1, value)
            visited_muds.add(order_node_pair(symmetric_0, symmetric_1))
            number_of_muds += 1
        return muds

    def _asymmetric(
        self,
        maze_config: MazeConfig,
        walls: Dict[Coordinates, List[Coordinates]],
    ) -> Dict[Coordinates, Dict[Coordinates, int]]:
        """
        Return a mud configuration without any constraints.
        Returns:
            The Dict of mud
        """
        possible_muds = self._possible_muds(maze_config, walls)
        muds: Dict[Coordinates, Dict[Coordinates, int]] = {}
        number_of_muds = 0
        random.shuffle(possible_muds)

        for mud in possible_muds:
            if number_of_muds / len(possible_muds) > maze_config.mud_density:
                break
            value = self._get_mud_value(maze_config.mud_range)
            add_mud(muds, mud[0], mud[1], value)
            number_of_muds += 1
        return muds

    def _get_mud_value(self, mud_range: int) -> int:
        """
        Returns:
            A random mud value in [2,self.mud_range]
        """
        return random.randint(2, mud_range)

    def _possible_muds(
        self, maze_config: MazeConfig, walls: Dict[Coordinates, List[Coordinates]]
    ) -> List[Tuple[Coordinates, Coordinates]]:
        mud_pairs: List[Tuple[Coordinates, Coordinates]] = []
        coordinates = product(range(maze_config.width), range(maze_config.height))
        # Create all possible muds
        for coordinate in coordinates:
            for neighbor in valid_neighbors(
                coordinate, maze_config.width, maze_config.height
            ):
                pair = (coordinate, neighbor)
                reverse_pair = (neighbor, coordinate)
                if (pair not in mud_pairs) and (reverse_pair not in mud_pairs):
                    mud_pairs.append(pair)
        # filter out where there are walls
        valid_muds = []
        for mud in mud_pairs:
            # There's not a wall
            if not _is_wall_present(mud[0], mud[1], walls):
                valid_muds.append(mud)
        return mud_pairs
