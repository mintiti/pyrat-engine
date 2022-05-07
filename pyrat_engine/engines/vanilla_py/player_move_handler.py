from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Coordinates, Move


def move(
    current_game_state: CurrentGameState, p1_move: Move, p2_move: Move
) -> CurrentGameState:

    # Update the mud status
    current_game_state.player1_mud -= 1
    current_game_state.player2_mud -= 1

    # Compute the destination cells
    is_player1_stuck = current_game_state.player1_mud > 0
    player1_destination = _compute_destination_cell(
        current_game_state=current_game_state,
        is_player_stuck=is_player1_stuck,
        player_position=current_game_state.player1_pos,
        move=p1_move,
    )
    is_player2_stuck = current_game_state.player2_mud > 0
    player2_destination = _compute_destination_cell(
        current_game_state=current_game_state,
        is_player_stuck=is_player2_stuck,
        player_position=current_game_state.player2_pos,
        move=p2_move,
    )

    # Update the misses status
    if current_game_state.player1_pos == player1_destination:
        current_game_state.player1_misses += 1
    if current_game_state.player2_pos == player2_destination:
        current_game_state.player2_misses += 1

    # TODO: Compute which cheeses have been taken
    # TODO: Compute the updated score

    return current_game_state
    # cell1 = cell_of_decision(player1_location, decision1)
    # cell2 = cell_of_decision(player2_location, decision2)
    # if cell1 in maze[player1_location]:
    #     stuck1 = maze[player1_location][cell1]
    #     player1_location = cell1
    #     moves1 = moves1 + 1
    # elif stuck1 <= 0:
    #     miss1 = miss1 + 1
    # if cell2 in maze[player2_location]:
    #     stuck2 = maze[player2_location][cell2]
    #     player2_location = cell2
    #     moves2 = moves2 + 1
    # elif stuck2 <= 0:
    #     miss2 = miss2 + 1
    # return player1_location, player2_location, stuck1, stuck2, moves1, moves2, miss1, miss2


def _compute_destination_cell(
    current_game_state: CurrentGameState,
    is_player_stuck: bool,
    player_position: Coordinates,
    move: Move,
) -> Coordinates:
    desired_destination_position = _get_desired_destination_position(
        player_position=player_position, move=move
    )

    # if the move is impossible, return the player's current position
    if not _is_move_possible(
        current_game_state=current_game_state,
        is_player_stuck=is_player_stuck,
        player_position=player_position,
        desired_destination_position=desired_destination_position,
    ):
        return player_position

    return desired_destination_position


def _get_desired_destination_position(
    player_position: Coordinates, move: Move
) -> Coordinates:
    x, y = player_position
    destination_cell = (x, y)
    if move == Move.UP:
        destination_cell = (x, y + 1)
    elif move == Move.LEFT:
        destination_cell = (x - 1, y)
    elif move == Move.DOWN:
        destination_cell = (x, y - 1)
    elif move == Move.RIGHT:
        destination_cell = (x + 1, y)
    return destination_cell


def _is_move_possible(
    current_game_state: CurrentGameState,
    is_player_stuck: bool,
    player_position: Coordinates,
    desired_destination_position: Coordinates,
) -> bool:
    # check if the player_position and the desired_destination are the same
    # or if the player is stuck
    if player_position == desired_destination_position or is_player_stuck:
        return False

    # check if the destination is inside the bounds of the maze
    dest_x, dest_y = desired_destination_position
    if (
        dest_x < 0
        or dest_x >= current_game_state.maze_width
        or dest_y < 0
        or dest_y >= current_game_state.maze_height
    ):
        return False

    # check if there is a wall between player position and destination position
    walls = current_game_state.walls
    if (
        desired_destination_position in walls[player_position]
        or player_position in walls[desired_destination_position]
    ):
        return False

    return True
