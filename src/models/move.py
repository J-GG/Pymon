from toolbox.i18n import I18n
from .exceptions.move_exception import MoveException


class Move:
    """A move in the game."""

    def __init__(self, id, type, category, power, accuracy, default_pp):
        """Creates a move.

        :param id: The id of the move.
        :param type: The ``EnumType`` indicating the type of the move.
        :param category: The ``MoveCategoryEnum`` indicating the category of
        the move.
        :param power: The power of the move.
        :param accuracy: The accuracy of the move (out of 100).
        :param default_pp: The default PP of the move.
        """

        if accuracy < 0 or accuracy > 100:
            raise MoveException("Incorrect accuracy: expected between "
                                "0 and 100 but got {0}".format(accuracy))

        self._id = id
        self._type = type
        self._category = category
        self._power = power
        self._accuracy = accuracy
        self._default_pp = default_pp

    @property
    def id(self):
        """Get the id of the move.

        :return: The id of the move.
        """

        return self._id

    @property
    def name(self):
        """Get the translated name of the move.

        :return: The name of the move.
        """

        return I18n().get("MOVE.{0}".format(self._id))

    @property
    def type(self):
        """Get the type of the move.

        The returned value is of ``TypeEnum`` type.
        :return: The type of the move.
        """

        return self._type

    @property
    def category(self):
        """Get the category of the move.

        The returned value is of ``MoveCategoryEnum`` type.
        :return: The category of the move.
        """

        return self._category

    @property
    def power(self):
        """Get the power of the move.

        The greater, the more damage it causes to the target.
        :return: The power of the move.
        """

        return self._power

    @property
    def accuracy(self):
        """Get the accuracy of this move out of 100.

        The greater, the more likely is the move to hit the target.
        When the accuracy is 100, it hits 100% of the time.
        :return: The accuracy of the the move.
        """

        return self._accuracy

    @property
    def default_pp(self):
        """Get the default number of power points.

        It is the number of times a pokemon can use this move when they
         learn it.
        :return: The default number of power points.
        """

        return self._default_pp
