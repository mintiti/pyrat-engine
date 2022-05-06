from typing import Generator, Iterable, List, Tuple

import random
from dataclasses import dataclass
from itertools import filterfalse, product

from pyrat_engine.initializer.configs import (
    CheeseMode,
    InitPlayerPosition,
    MazeConfig,
    PlayerConfig,
)
from pyrat_engine.types import Coordinates
from pyrat_engine.utils import central_symmetrical


@dataclass
class CheeseGenerator:
    p1_pos: Coordinates
    p2_pos: Coordinates

    def from_maze_config(self, maze_config: MazeConfig) -> List[Coordinates]:
        """Dispatch creating the cheese positions from a maze config
        Args:
            maze_config: The maze_config to parse

        Returns:
            A list of cheeses
        """
        cheese_list = []
        if maze_config.cheese_mode == CheeseMode.SYMMETRICAL:
            cheese_list = list(self.symmetric_cheeses_generator(maze_config))

        elif maze_config.cheese_mode == CheeseMode.ASYMMETRICAL:
            cheese_list = list(self.asymmetric_cheeses_generator(maze_config))

        elif maze_config.cheese_mode == CheeseMode.LIST:
            message: str = (
                "Maze configuration cheese_mode is CheeseMode.LIST, but no"
                + "cheeses were provided."
            )
            assert maze_config.cheeses, message
            cheese_list = maze_config.cheeses

        assert self.p1_pos not in cheese_list
        assert self.p2_pos not in cheese_list

        return cheese_list

    def symmetric_cheeses_generator(
        self, maze_config: MazeConfig
    ) -> Generator[Coordinates, None, None]:
        # width and height need to be odd if the number of cheeses is odd
        if maze_config.nb_cheese % 1:
            assert maze_config.width % 2 == 1 & maze_config.height % 2 == 1, (
                f"number of cheeses was {maze_config.nb_cheese}, which is odd,"
                f"but maze width and maze heights weren't odd.\n  "
            )
        # Not more cheeses than nb of cases
        assert maze_config.nb_cheese <= maze_config.width * maze_config.height

        nb_cheese = maze_config.nb_cheese
        width = maze_config.width
        height = maze_config.height
        # Initial pool of cheeses
        possible_cheeses: Iterable[Coordinates] = product(
            range(maze_config.width), range(maze_config.height)
        )
        # remove player positions and their symmetrical
        p1_symmetrical = (width - self.p1_pos[0] - 1, height - self.p1_pos[1] - 1)
        possible_cheeses = filterfalse(
            lambda x: (x == self.p1_pos or x == p1_symmetrical), possible_cheeses
        )

        p2_symmetrical = (width - self.p2_pos[0] - 1, height - self.p2_pos[1] - 1)
        possible_cheeses = filterfalse(
            lambda x: (x == self.p2_pos or x == p2_symmetrical), possible_cheeses
        )

        previous_cheeses_positions = set()
        # Edge case where nb_cheese is odd and width and height are also odd
        # There has to be a cheese in the middle
        if nb_cheese % 2 == 1:
            center_cheese = (width // 2, height // 2)
            yield center_cheese
            nb_cheese -= 1
            possible_cheeses = filterfalse(
                lambda x: x == center_cheese, possible_cheeses
            )

        possible_cheeses_list: List[Coordinates] = list(possible_cheeses)
        random.shuffle(possible_cheeses_list)

        for _ in range(0, nb_cheese // 2):
            cheese: Coordinates = possible_cheeses_list.pop()
            while cheese in previous_cheeses_positions:
                cheese = possible_cheeses_list.pop()

            # Add cheese to the previous ones and yield it
            previous_cheeses_positions.add(cheese)
            yield cheese

            # Add the symmetric to the previous ones and yield it
            symmetric_cheese = (width - cheese[0] - 1, height - cheese[1] - 1)
            previous_cheeses_positions.add(symmetric_cheese)
            yield symmetric_cheese

    def asymmetric_cheeses_generator(
        self, maze_config: MazeConfig
    ) -> Generator[Coordinates, None, None]:
        pass


class PlayerPositionGenerator:
    def __init__(self, maze_width: int, maze_height: int):
        self.maze_width: int = maze_width
        self.maze_height: int = maze_height

    def from_config(
        self, player_config: PlayerConfig
    ) -> Tuple[Coordinates, Coordinates]:
        """Create player positions from a config
        Args:
            player_config: PlayerConfig to respect

        Returns:
            the coordinates for each player
        """
        if player_config.player_pos_init == InitPlayerPosition.CORNER:
            return self._corner_positions()

        elif player_config.player_pos_init == InitPlayerPosition.SYMMETRIC:
            return self._symmetric()

        elif player_config.player_pos_init == InitPlayerPosition.ASYMMETRIC:
            return self._asymmetric()

        elif player_config.player_pos_init == InitPlayerPosition.CUSTOM:
            assert player_config.player1_pos is not None, (
                "player_pos_init is InitPlayerPosition.CUSTOM,"
                "but no player1_pos was provided."
            )
            assert player_config.player2_pos is not None, (
                "player_pos_init is InitPlayerPosition.CUSTOM,"
                "but no player2_pos was provided."
            )

            return player_config.player1_pos, player_config.player2_pos
        else:
            raise KeyError("Invalid player_pos_init key")

    def _corner_positions(self) -> Tuple[Coordinates, Coordinates]:
        return (0, 0), (self.maze_width - 1, self.maze_height - 1)

    def _symmetric(self) -> Tuple[Coordinates, Coordinates]:
        possible_positions: Iterable[Coordinates] = product(
            range(self.maze_width), range(self.maze_height)
        )

        # Edge case where there can be a perfect center of the maze
        if self.maze_width % 2 == 1 and self.maze_height % 2 == 1:
            middle = (self.maze_width // 2, self.maze_height // 2)
            possible_positions = filterfalse(lambda x: x == middle, possible_positions)

        possible_positions_list: List[Coordinates] = list(possible_positions)
        random.shuffle(possible_positions_list)
        return possible_positions_list[0], central_symmetrical(
            possible_positions_list[0],
            maze_width=self.maze_width,
            maze_height=self.maze_height,
        )

    def _asymmetric(self) -> Tuple[Coordinates, Coordinates]:
        possible_positions: Iterable[Coordinates] = product(
            range(self.maze_width), range(self.maze_height)
        )
        possible_positions_list: List[Coordinates] = list(possible_positions)
        return possible_positions_list[0], possible_positions_list[1]
