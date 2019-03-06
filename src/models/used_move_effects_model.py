import typing

from models.enumerations.move_effectiveness_enum import MoveEffectivenessEnum
from models.enumerations.staged_stat_enum import StagedStatEnum


class UsedMoveEffectsModel:
    """The effects of the move when used in a battle."""

    def __init__(self, failed: bool, hp: int, staged_stats: typing.Dict[StagedStatEnum, int],
                 effectiveness: MoveEffectivenessEnum, critical_hit: bool) -> None:
        """Create a new used move effects.

        :param failed: Whether the move failed or not.
        :param hp: The relative modification of HP. Can be greater or lower
        than 0.
        :param staged_stats: A dictionary with the modification on the staged
        stats.
        :param effectiveness: The effectiveness of the move.
        :param critical_hit: Whether the move is a critical hit or not.
        """

        self._failed = failed
        self._hp = hp
        self._staged_stats = staged_stats
        self._effectiveness = effectiveness
        self._critical_hit = critical_hit

    @property
    def failed(self) -> bool:
        """Get whether the move failed.

        :return: True if the move failed.
        """

        return self._failed

    @property
    def hp(self) -> int:
        """Get the HP effects of the move.

        :return: The HP effects of the move.
        """

        return self._hp

    @property
    def staged_stats(self) -> typing.Dict[StagedStatEnum, int]:
        """Get the staged stats effects of the move.

        :return: The staged stats effects of the move.
        """

        return self._staged_stats

    @property
    def effectiveness(self) -> MoveEffectivenessEnum:
        """Get the effectiveness of the move.

        :return: The effectiveness of the move.
        """

        return self._effectiveness

    @property
    def critical_hit(self) -> bool:
        """Whether the move is a critical hit.

        :return: True if it's a critical hit.
        """

        return self._critical_hit
