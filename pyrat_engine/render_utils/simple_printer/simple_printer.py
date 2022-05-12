from typing import Dict, List, Optional

from pyrat_engine.render_utils.base import Renderer
from pyrat_engine.render_utils.simple_printer import assets
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Coordinates, Move
from pyrat_engine.utils import down, left, right, up


class CurrentGameStateReader:
    def __init__(self, current_game_state: CurrentGameState):
        self.current_game_state = current_game_state
        self._init_matrix()
        self._init_intersections()

    @property
    def p1_score(self) -> float:
        return self.current_game_state.player1_score

    @property
    def p2_score(self):
        return self.current_game_state.player2_score

    def __getitem__(self, item: Coordinates):
        return self.cell_elements[item[0]][item[1]]

    def _init_matrix(self):
        """Initialize the contents of the cell"""
        maze_width = self.current_game_state.maze_width
        maze_height = self.current_game_state.maze_height
        # Initialize with nothing in the cells
        self.cell_elements: List[List[Optional[str]]] = [
            [assets.EMPTY] * maze_height for _ in range(maze_width)
        ]

        # Init cheeses :
        for cheese in self.current_game_state.current_cheese_list:
            self.cell_elements[cheese[0]][cheese[1]] = assets.CHEESE

    def _place_players(self):
        # Place the players
        if (
            self.current_game_state.player1_pos == self.current_game_state.player2_pos
            and self.current_game_state.player1_pos
            in self.current_game_state.current_cheese_list
        ):
            self.cell_elements[self.current_game_state.player1_pos[0]][
                self.current_game_state.player1_pos[1]
            ] = assets.RAT_AND_SNAKE_AND_CHEESE
        elif self.current_game_state.player1_pos == self.current_game_state.player2_pos:
            self.cell_elements[self.current_game_state.player1_pos[0]][
                self.current_game_state.player1_pos[1]
            ] = assets.RAT_AND_SNAKE
        else:
            if (
                self.current_game_state.player1_pos
                in self.current_game_state.current_cheese_list
            ):
                self.cell_elements[self.current_game_state.player1_pos[0]][
                    self.current_game_state.player1_pos[1]
                ] = assets.RAT_AND_CHEESE
            else:
                self.cell_elements[self.current_game_state.player1_pos[0]][
                    self.current_game_state.player1_pos[1]
                ] = assets.RAT
            if (
                self.current_game_state.player2_pos
                in self.current_game_state.current_cheese_list
            ):
                self.cell_elements[self.current_game_state.player2_pos[0]][
                    self.current_game_state.player2_pos[1]
                ] = assets.SNAKE_AND_CHEESE
            else:
                self.cell_elements[self.current_game_state.player2_pos[0]][
                    self.current_game_state.player2_pos[1]
                ] = assets.SNAKE

    def _init_intersections(self) -> None:
        """Initialize the intersections between cells"""
        maze_width = self.current_game_state.maze_width
        maze_height = self.current_game_state.maze_height
        self.intersections: Dict[Coordinates, Dict[Coordinates, str]] = {}
        for i in range(maze_width):
            for j in range(maze_height):
                coordinate = (i, j)
                up_intersection = self._get_intersection(coordinate, Move.UP)
                self.intersections[coordinate] = {up(coordinate): up_intersection}
                down_intersection = self._get_intersection(coordinate, Move.DOWN)
                self.intersections[coordinate][down(coordinate)] = down_intersection
                right_intersection = self._get_intersection(coordinate, Move.RIGHT)
                self.intersections[coordinate][right(coordinate)] = right_intersection
                left_intersection = self._get_intersection(coordinate, Move.LEFT)
                self.intersections[coordinate][left(coordinate)] = left_intersection

    def _intersection_between_coordinate_and_other(
        self, coordinate: Coordinates, other: Coordinates, is_horizontal: bool
    ) -> str:
        # There's a wall between the two cells
        walls = self.current_game_state.walls
        mud = self.current_game_state.mud
        if coordinate in walls and other in walls[coordinate]:
            return assets.HORIZONTAL_WALL if is_horizontal else assets.VERTICAL_WALL
        # There's mud between the two cells
        if coordinate in mud and other in mud[coordinate]:
            return assets.HORIZONTAL_MUD if is_horizontal else assets.VERTICAL_MUD
        return assets.EMPTY if is_horizontal else assets.VERTICAL_NOTHING

    def _get_intersection(self, coordinate: Coordinates, direction: Move):
        """Return the asset to represent the intersection between coordinate and the
        cell in direction"""
        if direction == Move.UP:
            return self._intersection_between_coordinate_and_other(
                coordinate, up(coordinate), is_horizontal=True
            )
        elif direction == Move.DOWN:
            return self._intersection_between_coordinate_and_other(
                coordinate, down(coordinate), is_horizontal=True
            )
        elif direction == Move.LEFT:
            return self._intersection_between_coordinate_and_other(
                coordinate, left(coordinate), is_horizontal=False
            )
        elif direction == Move.RIGHT:
            return self._intersection_between_coordinate_and_other(
                coordinate, right(coordinate), is_horizontal=False
            )
        return assets.EMPTY


class SimplePrinter(Renderer):
    def initialize(self) -> None:
        """Simple Printer doesn't acquire anything"""
        pass

    def close(self) -> None:
        """Simple Printer doesn't acquire anything"""
        pass

    def render(self, state: CurrentGameState) -> str:
        parser = CurrentGameStateReader(state)
        maze = self.make_maze(parser, state)
        p1_string = assets.PLAYER_SCORE_TEMPLATE.format(
            number=1,
            position=state.player1_pos,
            score=state.player1_score,
            mud=state.player1_mud,
            misses=state.player1_misses,
        )

        p2_string = assets.PLAYER_SCORE_TEMPLATE.format(
            number=2,
            position=state.player2_pos,
            score=state.player2_score,
            mud=state.player2_mud,
            misses=state.player2_misses,
        )
        ret = p1_string + "\n" + p2_string + maze
        print(ret)
        return ret

    def make_maze(self, parser, state):
        # indices :
        x_coordinates = "\n" + assets.EMPTY
        for i in range(state.maze_width):
            x_coordinates += assets.WALL_INTERSECTION + str(i).center(
                assets.ELEMENT_WIDTH
            )
        horizontal_limit = (
            assets.EMPTY
            + (assets.WALL_INTERSECTION + assets.HORIZONTAL_WALL) * state.maze_width
            + assets.WALL_INTERSECTION
        )
        maze = "\n" + horizontal_limit + x_coordinates
        # Compute the inside of the maze render
        for j in range(state.maze_height):
            cells = "\n" + f"{j}".center(assets.ELEMENT_WIDTH) + assets.VERTICAL_WALL
            upper_limit = "\n" + assets.EMPTY + assets.WALL_INTERSECTION
            for i in range(state.maze_width):
                coordinate = (i, j)
                cells += parser[coordinate]
                if i != state.maze_width - 1:
                    cells += parser.intersections[coordinate][right(coordinate)]
                else:
                    cells += assets.VERTICAL_WALL
                upper_limit += (
                    parser.intersections[coordinate][up(coordinate)]
                    + assets.WALL_INTERSECTION
                )
            maze = cells + maze
            if j != state.maze_height - 1:
                maze = upper_limit + maze
        maze = "\n" + horizontal_limit + maze
        return maze

    def __init__(self):
        pass
