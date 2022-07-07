from typing import List

import numpy as np
import numpy.typing as npt
from dataclasses import dataclass

from pyrat_engine.types import Coordinates, Move, Muds, Walls
from pyrat_engine.utils import get_direction


class Board:
    def __init__(
        self,
        maze_width: int,
        maze_height: int,
        p1_pos: Coordinates,
        p2_pos: Coordinates,
        walls: Walls,
        muds: Muds,
        cheeses: List[Coordinates],
    ):
        self.maze_width = maze_width
        self.maze_height = maze_height
        # width x height array with a True where there is a player
        # 0 is rat
        # 1 is snake
        # Array is in column major ('F') order because
        # most operations on this array are along the last dimension
        self.player_positions: npt.NDArray[bool] = np.zeros(
            (maze_width, maze_height, 2), dtype=bool, order="F"
        )
        self._init_player_positions(p1_pos, p2_pos)

        # self.can_move[x][y][Move.UP][0] gets whether we can go up
        # shape = (width, height, 5)
        self.can_move: npt.NDArray[bool] = self._create_labyrinth_boundaries()
        self._init_walls(walls)

        # self.cost[x][y][Move.UP] says how much turns it takes to go up
        self.cost: npt.NDArray[np.uint8] = np.ones(
            (maze_width, maze_height, 5), dtype=np.uint8, order="F"
        )  # max mud = 256 on uint8
        self._init_muds(muds)

        # self.cheeses[x][y] says whether there is a cheese in (x,y)
        # Order is set to column major order ('F') because
        # Most operations are done along the last dimension
        self.cheeses: npt.NDArray[bool] = np.zeros(
            (maze_width, maze_height), dtype=bool, order="F"
        )
        self._init_cheeses(cheeses)

    def _init_player_positions(self, p1_pos: Coordinates, p2_pos: Coordinates) -> None:
        """Place the players at the provided positions"""
        self.player_positions[p1_pos][0] = True
        self.player_positions[p2_pos][1] = True

    def _create_labyrinth_boundaries(self) -> npt.NDArray[bool]:
        """
        Create a can_move matrix with the 4 border walls of the labyrinth
        Returns:
            a can_move Matrix
        """
        can_move = np.ones(
            (self.maze_width, self.maze_height, 5), dtype=bool, order="F"
        )
        # Can't move up from upper row
        can_move[:, self.maze_height - 1, Move.UP] = False

        # Can't move down from lower row
        can_move[:, 0, Move.DOWN] = False

        # Can't move right from rightmost column
        can_move[self.maze_width - 1, :, Move.RIGHT] = False

        # Can't move left from leftmost column
        can_move[0, :, Move.LEFT] = False

        # Can't move with a null move
        can_move[:, :, Move.DID_NOT_MOVE] = False

        return can_move

    def _init_walls(self, walls: Walls) -> None:
        for coordinate, neighbours in walls.items():
            for neighbour in neighbours:
                move = get_direction(coordinate, neighbour)
                # Can't move from coordinate to neighbour
                self.can_move[coordinate][move] = False

                # opposite move
                opposite_move = get_direction(neighbour, coordinate)
                self.can_move[neighbour][opposite_move] = False

    def _init_muds(self, muds: Muds) -> None:
        """
        Initialize the cost matrix with the muds list
        Args:
            muds: Muds type dict, containing costs to go to the neighbours
        """
        for coordinate, neighbours in muds.items():
            for neighbour in neighbours:
                move = get_direction(coordinate, neighbour)
                self.cost[coordinate][move] = neighbours[neighbour]

    def _init_cheeses(self, cheeses: List[Coordinates]) -> None:
        for cheese in cheeses:
            self.cheeses[cheese] = True


@dataclass
class GameData:
    player_scores: npt.NDArray[float]
    player_muds: npt.NDArray[int]
    player_misses: npt.NDArray[int]


@dataclass
class NumpyState:
    board: Board
    game_data: GameData
