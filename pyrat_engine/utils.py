from typing import List

from pyrat_engine.types import Coordinates


def central_symmetrical(
    coordinate: Coordinates, maze_width, maze_height
) -> Coordinates:
    """Return the centrally symmetrical position of the coordinate in the maze
    Args:
        coordinate: the coordinates you want the central symmetry of
        maze_width: the width of the maze
        maze_height: the height of the maze

    Returns:
        The symmetrical coordinates.
    """
    return (maze_width - coordinate[0] - 1, maze_height - coordinate[1] - 1)


def up(coordinate: Coordinates) -> Coordinates:
    """
    Return the coordinate directly up of the given coordinate
    """
    return coordinate[0], coordinate[1] + 1


def down(coordinate: Coordinates) -> Coordinates:
    """
    Return the coordinate directly down of the given coordinate
    """
    return coordinate[0], coordinate[1] - 1


def left(coordinate: Coordinates) -> Coordinates:
    """
    Return the coordinate directly left of the given coordinate
    """
    return coordinate[0] - 1, coordinate[1]


def right(coordinate: Coordinates) -> Coordinates:
    """
    Return the coordinate directly right the given coordinate
    """
    return coordinate[0] + 1, coordinate[1]


def is_coordinate_valid(
    coordinate: Coordinates, maze_width: int, maze_height: int
) -> bool:
    """
    Return whether the coordinate is valid in a given maze size
    Args:
        coordinate: the coordinates of interest
        maze_width: the maximum width of the maze
        maze_height: the maximum height of the maze

    Returns:
        Whether the coordinate is valid in the maze
    """
    return 0 <= coordinate[0] < maze_width and 0 < coordinate[1] < maze_height


def neighbors(coordinate: Coordinates):
    """
    Make the list of neighbors of the coordinate, valid or not
    Args:
        coordinate: the coordinate of interest

    Returns:
        The list of neighbor coordinates
    """
    return [up(coordinate), down(coordinate), right(coordinate), left(coordinate)]


def valid_neighbors(
    coordinate: Coordinates, maze_width: int, maze_height: int
) -> List[Coordinates]:
    """
    Filter the neighbors of the coordinate to only keep the valid neighbors
    Args:
        coordinate: The coordinate of interest.
        maze_width: Width of the maze
        maze_height: Height of the maze

    Returns:
        The list of valid coordinates.
    """

    def validate_coordinate(coord: Coordinates) -> bool:
        return is_coordinate_valid(coord, maze_width, maze_height)

    return list(filter(validate_coordinate, neighbors(coordinate)))
