from enum import Enum
from math import floor


class ExperienceFunctionEnum(Enum):
    """Defines the learning curves.

    The amount of experience for a pokemon to reach a certain level is based on
    its level and one of these functions.
    """

    FAST = "FAST"
    MEDIUM_FAST = "MEDIUM_FAST"
    MEDIUM_SLOW = "MEDIUM_SLOW"
    SLOW = "SLOW"

    def __init__(self, value: str) -> None:
        """Create a new experience function.

        :param value: The name of the experience function.
        """

        super().__init__()
        self._value = value
        self._function = None

    def get_xp_for_level(self, level: int) -> int:
        """Get the number of points of experience necessary to reach the
        specified level.

        :param level: The level to reach.
        :return: the number of points of experience necessary to reach the
        level.
        """

        return self._function(level)


ExperienceFunctionEnum.FAST._function = lambda level: floor(4 * level ** 3 / 5)
ExperienceFunctionEnum.MEDIUM_FAST._function = lambda level: floor(level ** 3)
ExperienceFunctionEnum.MEDIUM_SLOW._function = lambda level: floor(
    6 / 5 * level ** 3 - 15 * level ** 2 + 100 * level - 140)
ExperienceFunctionEnum.SLOW._function = lambda level: floor(5 * level ** 3 / 4)
