from typing import Dict, List, Tuple

import random
from itertools import product

from pyrat_engine.initializer.configs import MazeConfig, MudMode
from pyrat_engine.types import Coordinates
from pyrat_engine.utils import central_symmetrical, valid_neighbors


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
    def __init__(self, maze_width: int, maze_height: int):
        self.maze_width = maze_width
        self.maze_height = maze_height

    def from_config(
        self, walls: Dict[Coordinates, List[Coordinates]], maze_config: MazeConfig
    ) -> Dict[Coordinates, Dict[Coordinates, int]]:
        """
        Dispatch creating the mud configuration from a maze configuration
        Args:
            walls: Walls that are already in the maze
            maze_config: The maze_config to parse

        Returns:
            A mud mapping
        """
        if maze_config.mud_mode == MudMode.RANDOM:
            return (
                self._symmetric(maze_config.mud_density, maze_config.mud_range, walls)
                if maze_config.symmetric
                else self._asymmetric(
                    maze_config.mud_density, maze_config.mud_range, walls
                )
            )
        else:
            assert (
                maze_config.mud is not None
            ), "mud_mode is MudMode.RANDOM, but not mud was provided."
            return maze_config.mud

    def _symmetric(
        self,
        mud_density: float,
        mud_range: int,
        walls: Dict[Coordinates, List[Coordinates]],
    ) -> Dict[Coordinates, Dict[Coordinates, int]]:
        """
        Return a symmetric mud configuration.
        Returns:
            The Mapping of mud
        """
        possible_muds = self._possible_muds(walls)
        muds: Dict[Coordinates, Dict[Coordinates, int]] = {}
        # Possible to make this better as there's extra work being done
        for mud in possible_muds:
            if random.random() > mud_density / 2:
                value = self._get_mud_value(mud_range)
                self._add_mud(muds, mud[0], mud[1], value)
                # Add the symmetrical mud
                symmetric_0 = central_symmetrical(
                    mud[0], self.maze_width, self.maze_height
                )
                symmetric_1 = central_symmetrical(
                    mud[1], self.maze_width, self.maze_height
                )
                self._add_mud(muds, symmetric_0, symmetric_1, value)
        return muds

    def _asymmetric(
        self,
        mud_density: float,
        mud_range: int,
        walls: Dict[Coordinates, List[Coordinates]],
    ) -> Dict[Coordinates, Dict[Coordinates, int]]:
        """
        Return a mud configuration without any constraints.
        Returns:
            The Mapping of mud
        """
        possible_muds = self._possible_muds(walls)
        muds: Dict[Coordinates, Dict[Coordinates, int]] = {}
        # Possible to make this better as there's extra work being done
        for mud in possible_muds:
            if random.random() > mud_density:
                value = self._get_mud_value(mud_range)
                self._add_mud(muds, mud[0], mud[1], value)
        return muds

    def _get_mud_value(self, mud_range: int) -> int:
        """
        Returns:
            A random mud value in [2,self.mud_range]
        """
        return random.randint(2, mud_range)

    def _add_mud(
        self,
        mud: Dict[Coordinates, Dict[Coordinates, int]],
        coordinate: Coordinates,
        neighbor: Coordinates,
        value: int,
    ) -> None:
        # Make sure the dicts exist in mud
        if coordinate not in mud:
            mud[coordinate] = {}
        if neighbor not in mud:
            mud[neighbor] = {}

        # Add the value to the dict
        mud[coordinate][neighbor] = value
        mud[neighbor][coordinate] = value

    def _possible_muds(
        self, walls: Dict[Coordinates, List[Coordinates]]
    ) -> List[Tuple[Coordinates, Coordinates]]:
        mud_pairs: List[Tuple[Coordinates, Coordinates]] = []
        coordinates = product(range(self.maze_width), range(self.maze_height))
        # Create all possible muds
        for coordinate in coordinates:
            neighbors = valid_neighbors(coordinate, self.maze_width, self.maze_height)
            for neighbor in neighbors:
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
