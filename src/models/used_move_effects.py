class UsedMoveEffects:
    """The effects of the move when used in a battle."""

    def __init__(self, failed, hp, staged_stats, effectiveness, critical_hit):
        self._failed = failed
        self._hp = hp
        self._staged_stats = staged_stats
        self._effectiveness = effectiveness
        self._critical_hit = critical_hit

    @property
    def failed(self):
        """Get whether the move failed.

        :return: True if the move failed.
        """

        return self._failed

    @property
    def hp(self):
        """Get the HP effects of the move.

        :return: The HP effects of the move.
        """

        return self._hp

    @property
    def staged_stats(self):
        """Get the staged stats effects of the move.

        :return: The staged stats effects of the move.
        """

        return self._staged_stats

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
