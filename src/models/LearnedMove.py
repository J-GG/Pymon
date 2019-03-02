class LearnedMove:
    """A move learned by a pokemon."""

    def __init__(self, move, pp, current_pp=None):
        """Creates a new learned move.

        :param move: The ``Move`` it refers to.
        :param pp: The maximal number of PP.
        :param current_pp: The current number of PP.
        """

        self._move = move
        self._pp = pp
        self._current_pp = current_pp if current_pp else pp

    @property
    def move(self):
        """Get the move the pokemon learned.

        :return: An instance of ``Move``.
        """

        return self._move

    @property
    def pp(self):
        """Get the number of maximal PP.

        :return: The number of maximal PP.
        """

        return self._pp

    @pp.setter
    def pp(self, pp):
        """Set the maximal number of PP.

        :param pp: The maximal number of PP.
        """

        self._pp = pp

    @property
    def current_pp(self):
        """Get the current number of PP.

        :return: The current number of PP.
        """

        return self._current_pp

    @current_pp.setter
    def current_pp(self, current_pp):
        """Set the current number of PP.

        :param current_pp: The current number of PP.
        """

        self._current_pp = current_pp
