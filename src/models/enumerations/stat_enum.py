from enum import Enum
from math import floor


class StatEnum(Enum):
    """Defines the types of pokemon stats and how to calculate them.

    The stats are calculated based on the base stat (same for all the pokemon
    of a species), the IV (depends on each pokemon) and their level.
    """

    HP = "HP"
    ATTACK = "Attack"
    DEFENSE = "Defense"
    SPECIAL_ATTACK = "Special attack"
    SPECIAL_DEFENSE = "Special defense"
    SPEED = "Speed"

    def __init__(self, value: str) -> None:
        """Create a new stat.

        :param value: The textual value of the enumeration.
        """

        super().__init__()
        self._value = value
        if value == "HP":
            self._function = lambda level, base_stat, iv: floor((2 * base_stat + iv) * level / 100 + level + 10)
        else:
            self._function = lambda level, base_stat, iv: floor(((2 * base_stat + iv) * level / 100 + 5) * 0.9)

    def get_stat(self, level: int, base_stat: int, iv: int) -> int:
        """Get the value of the stat for the indicated level based on the base stat
        of the pokemon and their IV.

        :param level: The level of the pokemon.
        :param base_stat: The base stat of the pokemon species.
        :param iv: The IV of the pokemon.
        :return: The stat.
        """

        return self._function(level, base_stat, iv)
