from typing import List, Tuple

from pyrat_engine.types import Coordinates, Move


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
    return 0 <= coordinate[0] < maze_width and 0 <= coordinate[1] < maze_height


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
    return [
        neighbor
        for neighbor in neighbors(coordinate)
        if is_coordinate_valid(neighbor, maze_width, maze_height)
    ]


def order_node_pair(
    node: Coordinates, other_node: Coordinates
) -> Tuple[Coordinates, Coordinates]:
    """
    Orders the pair of node to have a consitent representation of pairs of coordinates
    """
    return (node, other_node) if node <= other_node else (other_node, node)


def get_direction(coordinate: Coordinates, other: Coordinates) -> Move:
    """
    Return the move direction to get from coordinate to other
    Args:
        coordinate: coordinate we're starting from
        other: coordinate to get to

    Returns:
        The move type to get from coordinate to other
    """
    if other == coordinate:
        return Move.DID_NOT_MOVE
    elif other == up(coordinate):
        return Move.UP
    elif other == left(coordinate):
        return Move.LEFT
    elif other == down(coordinate):
        return Move.DOWN
    elif other == right(coordinate):
        return Move.RIGHT
    else:
        raise ValueError(f"Coordinates {coordinate} and {other} are not adjacent")
