import typing
from math import floor
from random import randint

from models.learned_move import LearnedMove
from models.pokemon_species import PokemonSpecies
from models.staged_stat_enum import StagedStatEnum
from models.stat_enum import StatEnum


class Pokemon:
    """A pokemon with their own characteristics.

    The ``stats`` designates the maximum value the stats of the pokemon
    can be (i.e. when no moves or items are altering them and when the HP are
    full).
    On the other hand, the ``current stats`` are based on the stats but may
    vary depending on the situation.
    """

    def __init__(self, species: PokemonSpecies, nickname: str, level: int, moves: [LearnedMove], hp: int = None,
                 experience: int = None, iv: typing.Dict[StatEnum, int] = None) -> None:
        """Create a new pokemon.

        :param species: The species of the pokemon.
        :param nickname: The nickname of the pokemon.
        :param level: The level of the pokemon.
        :param moves: The moves the pokemon has learned. A list of 4
        ``LearnedMove``.
        :param hp: The current HP of the pokemon.
        :param experience: The experience points of the pokemon. If None, it's
        determined based on the level.
        :param iv: The IV of the pokemon. A dictionary assigning a value from
        0 to 31 to each of the stats. If None, they are randomly generated.
        """

        self._species = species
        self._nickname = nickname
        self._level = level
        self._moves = moves
        self._experience = experience if experience else floor(species.experience_function.get_xp_for_level(level))
        self._update_experience_for_next_level()

        if iv:
            self._iv = iv
        else:
            self._iv = dict()
            for stat in StatEnum:
                self._iv[stat] = randint(0, 31)

        self._stats = dict()
        self._update_stats()
        self._hp = hp if hp else self._stats[StatEnum.HP]

        self._staged_stats = dict()
        for staged_stat in StagedStatEnum:
            self._staged_stats[staged_stat] = 0

    @property
    def species(self) -> PokemonSpecies:
        """Get the species of the pokemon.

        :return: An instance of ``PokemonSpecies``.
        """

        return self._species

    @property
    def nickname(self) -> str:
        """Get te nickname of the pokemon.

        :return: The nickname of the pokemon.
        """

        return self._nickname

    @nickname.setter
    def nickname(self, nickname: str) -> None:
        """Set the nickname of the pokemon.

        :param nickname: The nickname of the pokemon.
        """

        self._nickname = nickname

    @property
    def level(self) -> int:
        """Get the level of the pokemon.

        :return: The level of the pokemon.
        """

        return self._level

    @level.setter
    def level(self, level: int) -> None:
        """Set the level of the pokemon.

        :param level: The level of the pokemon.
        """

        self._level = level

    @property
    def staged_stats(self) -> typing.Dict[StagedStatEnum, int]:
        """Get the staged stats of the pokemon.

        :return: A dictionary of all staged stats with their value.
        """

        return self._staged_stats

    @staged_stats.setter
    def staged_stats(self, staged_stats: typing.Dict[StagedStatEnum, int]) -> None:
        """Set the stages stats of the pokemon.

        :param staged_stats: A dictionary of all the staged stats with their
        value.
        """

        self._staged_stats = staged_stats

    @property
    def moves(self) -> [LearnedMove]:
        """Get the moves the pokemon has learned.

        :return: A list of ``LearnedMove``.
        """

        return self._moves

    @moves.setter
    def moves(self, moves: [LearnedMove]) -> None:
        """Set the moves the pokemon has learned.

        :param moves: A list of ``LearnedMove``.
        """

        self._moves = moves

    @property
    def hp(self) -> int:
        """Get the current HP of the pokemon.

        :return: The current HP of the pokemon.
        """

        return self._hp

    @hp.setter
    def hp(self, hp: int) -> None:
        """Set the current HP of the pokemon.

        :param hp: The current HP of the pokemon.
        """

        self._hp = hp

    @property
    def stats(self) -> typing.Dict[StatEnum, int]:
        """Get the stats of the pokemon.

        :return: A dictionary of all stats with their maximum value.
        """

        return self._stats

    @stats.setter
    def stats(self, stats: typing.Dict[StatEnum, int]) -> None:
        """Set the stats of the pokemon.

        :param stats: A dictionary of all stats with their maximum value.
        """

        self._stats = stats

    @property
    def experience(self) -> int:
        """Get the number of experience points of the pokemon.

        :return: The number of experience points of the pokemon.
        """

        return self._experience

    @experience.setter
    def experience(self, experience: int) -> None:
        """Set the number of experience points of the pokemon.

        :param experience: The number of experience points of the pokemon.
        """

        self._experience = experience

    @property
    def experience_for_next_level(self) -> int:
        """Get the number of experience points needed to reach the next level.

        :return: The number of experience points needed to reach the
        next level.
        """
        return self._experience_for_next_level

    def _update_experience_for_next_level(self) -> None:
        """Determine the experience needed to reach the next level.
        """

        self._experience_for_next_level = floor(self.species.experience_function.get_xp_for_level(self.level + 1))

    def gain_experience(self, experience_gained: int) -> None:
        """Increase the number of experience points of the pokemon.

        If the number of XP is higher than the amount necessary to reach the
        next level, the pokemon levels up.

        :param experience_gained: The number of experience points gained.
        """

        self.experience += experience_gained
        while self.experience >= self._experience_for_next_level:
            self.level += 1
            self._update_stats()
            self._update_experience_for_next_level()

    def _update_stats(self) -> None:
        """Update the stats based on the level, the base stats and the IV of
        the pokemon.

        The HP increases proportionally to the old HP.
        """

        old_hp_stat = self._stats[StatEnum.HP] if StatEnum.HP in self._stats else None

        for stat in StatEnum:
            self._stats[stat] = stat.get_stat(self._level, self._species.base_stats[stat], self._iv[stat])

        self._hp = self._hp + old_hp_stat - self._stats[StatEnum.HP] if old_hp_stat and self._hp else self._stats[
            StatEnum.HP]
