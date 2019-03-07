from models.enumerations.move_category_enum import MoveCategoryEnum
from models.enumerations.type_enum import TypeEnum
from models.move_effects_model import MoveEffectsModel
from toolbox.i18n import I18n


class MoveModel:
    """A move in the game."""

    def __init__(self, id: str, move_type: TypeEnum, category: MoveCategoryEnum, power: int, accuracy: int,
                 default_pp: int,
                 effects: MoveEffectsModel = None) -> None:
        """Create a move.

        :param id: The id of the move.
        :param move_type: The ``EnumType`` indicating the type of the move.
        :param category: The ``MoveCategoryEnum`` indicating the category of
        the move.
        :param power: The power of the move.
        :param accuracy: The accuracy of the move (out of 100).
        :param default_pp: The default PP of the move.
        :param effects: The effects of the move.
        """

        self._id = id
        self._type = move_type
        self._category = category
        self._power = power
        self._accuracy = accuracy
        self._default_pp = default_pp
        self._effects = effects

    @property
    def id(self) -> str:
        """Get the id of the move.

        :return: The id of the move.
        """

        return self._id

    @property
    def name(self) -> str:
        """Get the translated name of the move.

        :return: The name of the move.
        """

        return I18n().get("MOVE.{0}".format(self._id))

    @property
    def type(self) -> TypeEnum:
        """Get the type of the move.

        The returned value is of ``TypeEnum`` type.
        :return: The type of the move.
        """

        return self._type

    @property
    def category(self) -> MoveCategoryEnum:
        """Get the category of the move.

        The returned value is of ``MoveCategoryEnum`` type.
        :return: The category of the move.
        """

        return self._category

    @property
    def power(self) -> int:
        """Get the power of the move.

        The greater, the more damage it causes to the target.
        :return: The power of the move.
        """

        return self._power

    @property
    def accuracy(self) -> int:
        """Get the accuracy of this move out of 100.

        The greater, the more likely is the move to hit the target.
        When the accuracy is 100, it hits 100% of the time.
        :return: The accuracy of the the move.
        """

        return self._accuracy

    @property
    def default_pp(self) -> int:
        """Get the default number of power points.

        It is the number of times a pokemon can use this move when they
         learn it.
        :return: The default number of power points.
        """

        return self._default_pp

    @property
    def effects(self) -> MoveEffectsModel:
        """Get the effects of the move.

        :return: A ``MoveEffectsModel``.
        """

        return self._effects
