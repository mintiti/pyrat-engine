from pyrat_engine.types import Coordinates


def central_symmetrical(coordinate: Coordinates, maze_width, maze_height) -> Coordinates:
    """Return the centrally symmetrical position of the coordinate in the maze
    Args:
        coordinate: the coordinates you want the central symmetry of
        maze_width: the width of the maze
        maze_height: the height of the maze

    Returns:
        The symmetrical coordinates.
    """
    return (maze_width - coordinate[0] - 1, maze_height - coordinate[1] - 1)
