class MoveEffects:
    """The effects of the move when used in a battle."""

    def __init__(self, failed, stats, effectiveness, critical_hit):
        self._failed = failed
        self._stats = stats
        self._effectiveness = effectiveness
        self._critical_hit = critical_hit

    @property
    def failed(self):
        """Get whether the move failed.

        :return: True if the move failed.
        """

        return self._failed

    @property
    def stats(self):
        """Get the stats effects of the move.

        :return: The stats effects of the move.
        """

        return self._stats

    @property
    def effectiveness(self):
        """Get the effectiveness of the move.

        :return: The effectiveness of the move.
        """

        return self._effectiveness

    @property
    def critical_hit(self):
        """Whether the move is a critical hit.

        :return: True if it's a critical hit.
        """

        return self._critical_hit
