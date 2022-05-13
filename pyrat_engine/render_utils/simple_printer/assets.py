ELEMENT_WIDTH = 5

RAT = "\033[1;31m" + "R".center(ELEMENT_WIDTH) + "\033[0m"
SNAKE = "\033[1;32m" + "S".center(ELEMENT_WIDTH) + "\033[0m"
RAT_AND_SNAKE = "\033[1;31m" + "RS".center(ELEMENT_WIDTH) + "\033[0m"
CHEESE = "C".center(ELEMENT_WIDTH)
RAT_AND_CHEESE = "\033[1;31m" + "RC".center(ELEMENT_WIDTH) + "\033[0m"
SNAKE_AND_CHEESE = "\033[1;32m" + "SC".center(ELEMENT_WIDTH) + "\033[0m"
RAT_AND_SNAKE_AND_CHEESE = "\033[1;31m" + "RSC".center(ELEMENT_WIDTH) + "\033[0m"
EMPTY = "".center(ELEMENT_WIDTH)
VERTICAL_WALL = "|"
VERTICAL_MUD = "┊"
VERTICAL_NOTHING = " "
HORIZONTAL_WALL = "―――".center(ELEMENT_WIDTH)
HORIZONTAL_MUD = "┈┈┈".center(ELEMENT_WIDTH)
WALL_INTERSECTION = "+"

PLAYER_SCORE_TEMPLATE = """\033[1mPlayer {number} state:\033[0m
    Position : {position}
    Score : {score}
    Mud : {mud}
    Misses : {misses}\n"""
