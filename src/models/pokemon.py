from math import floor
from random import randint

from models.stat_enum import StatEnum


class Pokemon:
    """A pokemon with their own characteristics.

    The ``stats`` designates the maximum value the stats of the pokemon
    can be (i.e. when no moves or items are altering them and when the HP are
    full).
    On the other hand, the ``current stats`` are based on the stats but may
    vary depending on the situation.
    """

    def __init__(self, species, nickname, level, moves, experience=None, iv=None):
        """Creates a new pokemon.

        :param species: The species of the pokemon. An instance of
        ``PokemonSpecies``
        :param nickname: The nickname of the pokemon.
        :param level: The level of the pokemon.
        :param moves: The moves the pokemon has learned. A list of 4
        ``LearnedMove``.
        :param experience: The experience points of the pokemon. If None, it's
        determined based on the level.
        :param iv: The IV of the pokemon. A dictionary assigning a value from
        0 to 31 to each of the stats. If None, they are randomly generated.
        """

        self._species = species
        self._nickname = nickname
        self._level = level
        self._moves = moves
        self._experience = experience if experience else floor(species.experienceFunction.get_xp_for_level(level))
        self._update_experience_for_next_level()

        if iv:
            self._iv = iv
        else:
            self._iv = dict()
            for stat in StatEnum:
                self._iv[stat.name] = randint(0, 31)

        self._stats = dict()
        self._current_stats = dict()
        self._update_stats()

    @property
    def species(self):
        """Get the species of the pokemon.

        :return: An instance of ``PokemonSpecies``.
        """

        return self._species

    @property
    def nickname(self):
        """Get te nickname of the pokemon.

        :return: The nickname of the pokemon.
        """

        return self._nickname

    @nickname.setter
    def nickname(self, nickname):
        """Set the nickname of the pokemon.

        :param nickname: The nickname of the pokemon.
        """

        self._nickname = nickname

    @property
    def level(self):
        """Get the level of the pokemon.

        :return: The level of the pokemon.
        """

        return self._level

    @level.setter
    def level(self, level):
        """Set the level of the pokemon.

        :param level: The level of the pokemon.
        """

        self._level = level

    @property
    def current_stats(self):
        """Get the current stats of the pokemon.

        :return: A dictionary of all stats with their current value.
        """

        return self._current_stats

    @current_stats.setter
    def current_stats(self, current_stats):
        """Set the current stats of the pokemon.

        :param current_stats: The current stats of the pokemon.
        """

        self._current_stats = current_stats

    @property
    def moves(self):
        """Get the moves the pokemon has learned.

        :return: A list of ``LearnedMove``.
        """

        return self._moves

    @moves.setter
    def moves(self, moves):
        """Set the moves the pokemon has learned.

        :param moves: A list of ``LearnedMove``.
        """

        self._moves = moves

    @property
    def stats(self):
        """Get the stats of the pokemon.

        :return: A dictionary of all stats with their maximum value.
        """

        return self._stats

    @stats.setter
    def stats(self, stats):
        """Set the stats of the pokemon.

        :param stats: A dictionary of all stats with their maximum value.
        """

        self._stats = stats

    @property
    def experience(self):
        """Get the number of experience points of the pokemon.

        :return: The number of experience points of the pokemon.
        """

        return self._experience

    @experience.setter
    def experience(self, experience):
        """Set the number of experience points of the pokemon.

        :param experience: The number of experience points of the pokemon.
        """
        self._experience = experience

    def _update_experience_for_next_level(self):
        """Determine the experience needed to reach the next level.
        """

        self._experience_for_next_level = floor(self.species.experience_function.function(self.level + 1))

    def gain_experience(self, experience_gained):
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

    def _update_stats(self):
        """Update the stats and the current stats based on the level, the base
        stats and the IV of the pokemon.

        The current stats increases proportionally to the old current stats and
        the stats
        """

        for stat in StatEnum:
            stat_value = stat.function(self.level, self.species.baseStats[stat.name], self.iv[stat.name])
            if stat.name in self.current_stats and stat.name in self.stats:
                self.current_stats[stat.name] += stat_value - self.stats[stat.name]
            else:
                self.current_stats[stat.name] = stat_value

            self.stats[stat.name] = stat.function(self.level, self.species.baseStats[stat.name], self.iv[stat.name])
