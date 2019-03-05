import random

from models.staged_stat_enum import StagedStatEnum
from models.stat_enum import StatEnum
from toolbox.i18n import I18n
from .move_category_enum import MoveCategoryEnum
from .used_move_effects import UsedMoveEffects


class Move:
    """A move in the game."""

    def __init__(self, id, move_type, category, power, accuracy, default_pp, effects=None):
        """Creates a move.

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

    def effects(self, attacker, defender):
        """Apply the effects of the move based on the attacked who used the
        move and the defender.

        :param attacker: The pokemon who used the move.
        :param defender: The pokemon receiving the move.
        :return: A ``UsedMoveEffects``containing the result of the move.
        """

        failed = random.randint(1, 100) > self._accuracy
        effectiveness = None
        critical_multiplier = None
        staged_stats = None
        hp = 0

        if not failed:
            if self.category in [MoveCategoryEnum.PHYSICAL, MoveCategoryEnum.SPECIAL]:
                if self._category == MoveCategoryEnum.PHYSICAL:
                    attack = attacker.stats[StatEnum.ATTACK] * StagedStatEnum.ATTACK.get_multiplier(
                        attacker.staged_stats[StagedStatEnum.ATTACK])
                    defense = defender.stats[StatEnum.DEFENSE] * StagedStatEnum.DEFENSE.get_multiplier(
                        defender.staged_stats[StagedStatEnum.DEFENSE])
                else:
                    attack = attacker.stats[StatEnum.SPECIAL_ATTACK] * StagedStatEnum.SPECIAL_ATTACK.get_multiplier(
                        attacker.staged_stats[StagedStatEnum.SPECIAL_ATTACK])
                    defense = defender.stats[StatEnum.SPECIAL_ATTACK] * StagedStatEnum.SPECIAL_DEFENSE.get_multiplier(
                        defender.staged_stats[StagedStatEnum.SPECIAL_DEFENSE])

                effectiveness = self.type.effectiveness(defender.species.type)
                critical_multiplier = 1.5 if random.randint(1, 256) <= attacker.stats[
                    StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
                    attacker.staged_stats[StagedStatEnum.SPEED]) / 2 else 1
                modifier = critical_multiplier * effectiveness.value * random.uniform(0.85, 1)
                hp = -round(((2 * attacker.level / 5 + 2) * self._power * attack / defense / 50 + 5) * modifier)

            staged_stats = self._effects.staged_stats if self._effects else None

        return UsedMoveEffects(failed, hp, staged_stats, effectiveness, critical_multiplier == 1.5)
