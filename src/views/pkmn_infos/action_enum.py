from enum import Enum


class ActionEnum(Enum):
    """The list of actions available to the player in a PKMN infos scene."""

    PREVIOUS = 0
    SHIFT = 1
    CANCEL = 2
    NEXT = 3
    MOVE_1 = 4
    MOVE_2 = 5
    MOVE_3 = 6
    MOVE_4 = 7
    NEW_MOVE = 8
