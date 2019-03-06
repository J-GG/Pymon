import typing

from models.enumerations.staged_stat_enum import StagedStatEnum
from models.enumerations.status_enum import StatusEnum


class MoveEffectsModel:
    """The effects of a move."""

    def __init__(self, staged_stats: typing.Dict[StagedStatEnum, int], status: typing.Dict[StatusEnum, int]) -> None:
        """Create a new move effects.

        :param staged_stats: A dictionary of all the staged stats altered with
        their value.
        :param status:A dictionary of all the status altered with their value.
        """

        self._staged_stats = staged_stats
        self._status = status

    @property
    def staged_stats(self) -> typing.Dict[StagedStatEnum, int]:
        """Get the staged stats effects of the move.

        :return: The staged stats effects of the move.
        """

        return self._staged_stats

    @property
    def status(self) -> typing.Dict[StatusEnum, int]:
        """Get the status effects of the move.

        :return: The status effects of the move.
        """

        return self._status
