class MoveEffects:
    """The effects of a move."""

    def __init__(self, staged_stats, status):
        self._staged_stats = staged_stats
        self._status = status

    @property
    def staged_stats(self):
        """Get the staged stats effects of the move.

        :return: The staged stats effects of the move.
        """

        return self._staged_stats

    @property
    def status(self):
        """Get the status effects of the move.

        :return: The status effects of the move.
        """

        return self._status
