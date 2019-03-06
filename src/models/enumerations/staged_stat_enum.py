import typing
from enum import Enum


class StagedStatEnum(Enum):
    """Defines the types of staged stats. They differ from the stats as ``HP`` is
    not included but ``ACCURACY`` is added.

    The stage of a stat is a multiplier increasing or decreasing the value of
    a stat. It can take a value between -6 and +6.
    """

    ATTACK = "attack", {-6: 2 / 8, -5: 2 / 7, -4: 2 / 6, -3: 2 / 5, -2: 2 / 4, -1: 2 / 3, 0: 2 / 2, 1: 3 / 2, 2: 4 / 2,
                        3: 5 / 2,
                        4: 6 / 2, 5: 7 / 2, 6: 8 / 2}
    DEFENSE = "defense", {-6: 2 / 8, -5: 2 / 7, -4: 2 / 6, -3: 2 / 5, -2: 2 / 4, -1: 2 / 3, 0: 2 / 2, 1: 3 / 2,
                          2: 4 / 2,
                          3: 5 / 2, 4: 6 / 2, 5: 7 / 2, 6: 8 / 2}
    SPECIAL_ATTACK = "special attack", {-6: 2 / 8, -5: 2 / 7, -4: 2 / 6, -3: 2 / 5, -2: 2 / 4, -1: 2 / 3, 0: 2 / 2,
                                        1: 3 / 2, 2: 4 / 2,
                                        3: 5 / 2, 4: 6 / 2, 5: 7 / 2, 6: 8 / 2}
    SPECIAL_DEFENSE = "special defense", {-6: 2 / 8, -5: 2 / 7, -4: 2 / 6, -3: 2 / 5, -2: 2 / 4, -1: 2 / 3, 0: 2 / 2,
                                          1: 3 / 2, 2: 4 / 2,
                                          3: 5 / 2, 4: 6 / 2, 5: 7 / 2, 6: 8 / 2}
    SPEED = "speed", {-6: 2 / 8, -5: 2 / 7, -4: 2 / 6, -3: 2 / 5, -2: 2 / 4, -1: 2 / 3, 0: 2 / 2, 1: 3 / 2, 2: 4 / 2,
                      3: 5 / 2, 4: 6 / 2, 5: 7 / 2, 6: 8 / 2}
    ACCURACY = "accuracy", {-6: 3 / 9, -5: 3 / 8, -4: 3 / 7, -3: 3 / 6, -2: 3 / 5, -1: 3 / 4, 0: 3 / 3, 1: 4 / 3,
                            2: 5 / 3,
                            3: 6 / 3, 4: 7 / 3, 5: 8 / 3, 6: 9 / 3}

    def __init__(self, value: str, multipliers: typing.Dict[int, float]) -> None:
        """Create a new staged stat.

        :param value The textual value of the enumeration.
        :param multipliers A dictionary with stages as keys and multipliers as
        values.
        """

        super().__init__()
        self._value = value
        self._multipliers = multipliers

    def get_multiplier(self, stage: int) -> float:
        """Get the multiplier for the given stage.

        :param stage: The stage of the stat.
        """

        return self._multipliers[stage]
