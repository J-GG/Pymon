from enum import Enum


class PlayerActionEnum(Enum):
    """List of available actions to the user on the map."""

    ACTION_BUTTON = 0
    PLAYER_START_MOVE = 1
    PLAYER_END_MOVE = 2
