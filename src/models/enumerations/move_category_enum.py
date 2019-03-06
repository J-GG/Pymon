from enum import Enum


class MoveCategoryEnum(Enum):
    """The three categories of moves:
    - PHYSICAL: Damage calculation based on the user's attack and the target's
        defense.
    - SPECIAL: Damage calculation based on the user's special attack and
        the target's defense.
    - STATUS: Doesn't inflict damage but can inflict status conditions or
        raise or lower the stats of a pokemon among other effects.
    """

    PHYSICAL = "Physical"
    SPECIAL = "Special"
    STATUS = "Status"
