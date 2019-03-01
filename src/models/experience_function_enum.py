from enum import Enum
from math import floor


class ExperienceFunctionEnum(Enum):
    """Defines the learning curves.

    The amount of experience for a pokemon to reach a certain level is based on
    its level and one of these functions.
    """

    FAST = "FAST", lambda level: floor(4 * level ** 3 / 5)
    MEDIUM_FAST = "MEDIUM_FAST", lambda level: floor(level ** 3)
    MEDIUM_SLOW = "MEDIUM_SLOW", lambda level: floor(6 / 5 * level ** 3 - 15 * level ** 2 + 100 * level - 140)
    SLOW = "SLOW", lambda level: floor(5 * level ** 3 / 4)

    def __init__(self, value, function):
        self._value = value
        self._function = function

    def get_xp_for_level(self, level):
        """Get the number of points of experience necessary to reach the
        specified level.

        :param level: The level to reach.
        :return: the number of points of experience necessary to reach the level.
        """
        return self._function(level)
