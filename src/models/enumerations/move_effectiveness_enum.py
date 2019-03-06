from enum import Enum


class MoveEffectivenessEnum(Enum):
    """The list of effectiveness of a move.

    The value represents the multiplier of the damage caused by the move.
    """

    NORMAL = 1
    NO_EFFECT = 0
    VERY_INEFFECTIVE = 1 / 4
    NOT_EFFECTIVE = 1 / 2
    SUPER_EFFECTIVE = 2
    EXTREMELY_EFFECTIVE = 4
