from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Coordinates, Move


def move(
    current_game_state: CurrentGameState, p1_move: Move, p2_move: Move
) -> CurrentGameState:

    # Remove 1 to the mud status at the start of the turn (technically this could
    # overflow, but it would be very unlikely that a game have 2 ** 31 turns)
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

    _update_misses(
        current_game_state=current_game_state,
        player1_destination=player1_destination,
        player2_destination=player2_destination,
    )
    _update_mud_status(
        current_game_state=current_game_state,
        player1_destination=player1_destination,
        player2_destination=player2_destination,
    )
    _update_players_position(
        current_game_state=current_game_state,
        player1_destination=player1_destination,
        player2_destination=player2_destination,
    )
    _update_cheeses_and_score(current_game_state=current_game_state)

    return current_game_state


def _update_cheeses_and_score(current_game_state: CurrentGameState):
    pos1, pos2, cheeses = (
        current_game_state.player1_pos,
        current_game_state.player2_pos,
        current_game_state.current_cheese_list,
    )
    if pos1 == pos2 and pos1 in cheeses:
        cheeses.remove(pos1)
        current_game_state.player1_score += 0.5
        current_game_state.player2_score += 0.5
    if pos1 in cheeses:
        cheeses.remove(pos1)
        current_game_state.player1_score += 1
    if pos2 in cheeses:
        cheeses.remove(pos2)
        current_game_state.player2_score += 1
    return


def _update_players_position(
    current_game_state: CurrentGameState,
    player1_destination: Coordinates,
    player2_destination: Coordinates,
):
    current_game_state.player1_pos = player1_destination
    current_game_state.player2_pos = player2_destination
    return


def _update_mud_status(
    current_game_state: CurrentGameState,
    player1_destination: Coordinates,
    player2_destination: Coordinates,
):

    if current_game_state.player1_mud <= 0:
        current_game_state.player1_mud = current_game_state.mud.get(
            current_game_state.player1_pos, {}
        ).get(player1_destination, 0)

    if current_game_state.player2_mud <= 0:
        current_game_state.player2_mud = current_game_state.mud.get(
            current_game_state.player2_pos, {}
        ).get(player2_destination, 0)
    return


def _update_misses(
    current_game_state: CurrentGameState,
    player1_destination: Coordinates,
    player2_destination: Coordinates,
):
    # Update the misses status
    if current_game_state.player1_pos == player1_destination:
        current_game_state.player1_misses += 1
    if current_game_state.player2_pos == player2_destination:
        current_game_state.player2_misses += 1
    return


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
    if move == Move.UP:
        return x, y + 1
    elif move == Move.LEFT:
        return x - 1, y
    elif move == Move.DOWN:
        return x, y - 1
    elif move == Move.RIGHT:
        return x + 1, y
    return x, y


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
