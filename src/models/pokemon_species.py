from toolbox.i18n import I18n
from .exceptions.pokemon_species_exception import PokemonSpeciesException


class PokemonSpecies:
    """A species of pokemon."""

    def __init__(self, id, type, moves_by_lvl_up, base_stats, base_experience, experience_function):
        """Creates a new pokemon species.

        :param id: The id of the species.
        :param type: A list of ``EnumType``
        :param moves_by_lvl_up: A dictionary of moves learned by leveling up.
         The key is the level and the value is a list of moves id.
        :param base_stats: A dictionary of base stats.
        The key is a value of ``StatEnum`` and the value an int.
        :param base_experience: The base experience of the species.
        :param experience_function: The experience function to determine the
        experience necessary to reach a certain level.
        An instance of ``ExperienceFunctionEnum``
        """

        if len(type) > 2:
            raise PokemonSpeciesException("Too many types: 1 or 2 expected but "
                                          "got {0}".format(len(type)))

        self._id = id
        self._type = type
        self._moves_by_lvl_up = moves_by_lvl_up
        self._base_stats = base_stats
        self._base_experience = base_experience
        self._experience_function = experience_function

    @property
    def id(self):
        """Get the id of the pokemon species.

        The id can be used to get the translated name of the species.
        :return: The id of the pokemon species.
        """
        return self._id

    @property
    def name(self):
        """Get the translated name of the species.

        :return: The name of the species.
        """

        return I18n().get("POKEMON.{0}".format(self._id))

    @property
    def type(self):
        """Get the types (1 or 2) of the pokemon.

        The list contains values of ``TypeEnum`` type.
        :return: A list of types.
        """
        return self._type

    @property
    def moves_by_lvl_up(self):
        """Get the dictionary of moves which can be learned by leveling up.

        The key is the level and the value is a list of moves id.
        :return: A dictionary of moves.
        """
        return self._moves_by_lvl_up

    @property
    def base_stats(self):
        """Get the dictionary of base stats.

        The key is a value of ``StatEnum`` and the value an int.
        :return: A dictionary of base stats.
        """
        return self._base_stats

    @property
    def base_experience(self):
        """Get the base experience.

        :return: The base experience.
        """
        return self._base_experience

    @property
    def experience_function(self):
        """The experience function to determine the experience necessary to
        reach a certain level.

        :return: An instance of ``ExperienceFunctionEnum``
        """
        return self._experience_function
