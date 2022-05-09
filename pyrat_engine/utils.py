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
