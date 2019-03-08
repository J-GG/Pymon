import typing

from models.enumerations.experience_function_enum import ExperienceFunctionEnum
from models.enumerations.stat_enum import StatEnum
from models.enumerations.type_enum import TypeEnum
from models.move_model import MoveModel
from toolbox.i18n import I18n


class PokemonSpeciesModel:
    """A species of pokemon."""

    def __init__(self, id: str, type: typing.List[TypeEnum], moves_by_lvl_up: typing.Dict[int, typing.List[MoveModel]],
                 base_stats: typing.Dict[StatEnum, int], base_experience: int,
                 experience_function: ExperienceFunctionEnum) -> None:
        """Create a new pokemon species.

        :param id: The id of the species.
        :param type: A list of ``EnumType``
        :param moves_by_lvl_up: A dictionary of moves learned by leveling up.
         The key is the level and the value is a list of ``Move``.
        :param base_stats: A dictionary of base stats.
        The key is a value of ``StatEnum`` and the value an int.
        :param base_experience: The base experience of the species.
        :param experience_function: The experience function to determine the
        experience necessary to reach a certain level.
        An instance of ``ExperienceFunctionEnum``
        """

        self._id = id
        self._type = type
        self._moves_by_lvl_up = moves_by_lvl_up
        self._base_stats = base_stats
        self._base_experience = base_experience
        self._experience_function = experience_function

    @property
    def id(self) -> str:
        """Get the id of the pokemon species.

        The id can be used to get the translated name of the species.
        :return: The id of the pokemon species.
        """
        return self._id

    @property
    def name(self) -> str:
        """Get the translated name of the species.

        :return: The name of the species.
        """

        return I18n().get("POKEMON.{0}".format(self._id))

    @property
    def type(self) -> typing.List[TypeEnum]:
        """Get the types (1 or 2) of the pokemon.

        The list contains values of ``TypeEnum`` type.
        :return: A list of types.
        """
        return self._type

    @property
    def moves_by_lvl_up(self) -> typing.Dict[int, typing.List[MoveModel]]:
        """Get the dictionary of moves which can be learned by leveling up.

        The key is the level and the value is a list of moves id.
        :return: A dictionary of moves.
        """
        return self._moves_by_lvl_up

    @property
    def base_stats(self) -> typing.Dict[StatEnum, int]:
        """Get the dictionary of base stats.

        The key is a value of ``StatEnum`` and the value an int.
        :return: A dictionary of base stats.
        """
        return self._base_stats

    @property
    def base_experience(self) -> int:
        """Get the base experience.

        :return: The base experience.
        """
        return self._base_experience

    @property
    def experience_function(self) -> ExperienceFunctionEnum:
        """The experience function to determine the experience necessary to
        reach a certain level.

        :return: An instance of ``ExperienceFunctionEnum``
        """
        return self._experience_function
