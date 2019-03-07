import random

from models.battle.used_move_effects_model import UsedMoveEffectsModel
from models.enumerations.move_category_enum import MoveCategoryEnum
from models.enumerations.staged_stat_enum import StagedStatEnum
from models.enumerations.stat_enum import StatEnum
from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel


class FightActionModel:
    """Represents the use of a move during a battle."""

    def __init__(self, attacker: PokemonModel, defender: PokemonModel, move: LearnedMoveModel) -> None:
        """Create a new fight action.

        :param attacker: The attacking pokemon.
        :param defender: The defending pokemon.
        :param move: The move used by the attacker against the defender.
        """

        self._attacker = attacker
        self._defender = defender
        self._move = move
        self._effects = None

    @property
    def attacker(self) -> PokemonModel:
        """Get the attacking pokemon.

        :return: The ``PokemonModel`` of the attacking pokemon.
        """

        return self._attacker

    @property
    def defender(self) -> PokemonModel:
        """Get the defending pokemon.

        :return: The ``PokemonModel`` of the defending pokemon.
        """

        return self._defender

    @property
    def move(self) -> LearnedMoveModel:
        """Get the move the attacked used.

        :return: The ``LearnedMoveModel`` of the used move.
        """

        return self._move

    def get_effects(self) -> UsedMoveEffectsModel:
        """Apply the effects of the move based on the attacked who used the
         move and the defender.

         :return: A ``UsedMoveEffects``containing the result of the move.
         """

        if self._effects is None:
            failed = random.randint(1, 100) > self._move.move.accuracy * StagedStatEnum.ACCURACY.get_multiplier(
                self._attacker.staged_stats[StagedStatEnum.ACCURACY]) if self._move.move.accuracy else False
            effectiveness = None
            critical_multiplier = None
            staged_stats = dict()
            hp = 0

            if not failed:
                if self._move.move.category in [MoveCategoryEnum.PHYSICAL, MoveCategoryEnum.SPECIAL]:
                    if self._move.move.category == MoveCategoryEnum.PHYSICAL:
                        attack = self._attacker.stats[StatEnum.ATTACK] * StagedStatEnum.ATTACK.get_multiplier(
                            self._attacker.staged_stats[StagedStatEnum.ATTACK])
                        defense = self._defender.stats[StatEnum.DEFENSE] * StagedStatEnum.DEFENSE.get_multiplier(
                            self._defender.staged_stats[StagedStatEnum.DEFENSE])
                    else:
                        attack = self._attacker.stats[
                                     StatEnum.SPECIAL_ATTACK] * StagedStatEnum.SPECIAL_ATTACK.get_multiplier(
                            self._attacker.staged_stats[StagedStatEnum.SPECIAL_ATTACK])
                        defense = self._defender.stats[
                                      StatEnum.SPECIAL_ATTACK] * StagedStatEnum.SPECIAL_DEFENSE.get_multiplier(
                            self._defender.staged_stats[StagedStatEnum.SPECIAL_DEFENSE])

                    effectiveness = self._move.move.type.effectiveness(self._defender.species.type)
                    critical_multiplier = 1.5 if random.randint(1, 256) <= self._attacker.stats[
                        StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
                        self._attacker.staged_stats[StagedStatEnum.SPEED]) / 2 else 1
                    modifier = critical_multiplier * effectiveness.value * random.uniform(0.85, 1)
                    hp = -round(
                        ((
                                 2 * self._attacker.level / 5 + 2) * self._move.move.power * attack / defense / 50 + 5) * modifier)

                staged_stats = self._move.move.effects.staged_stats if self._move.move.effects else dict()

            self._effects = UsedMoveEffectsModel(failed, hp, staged_stats, effectiveness, critical_multiplier == 1.5)

        return self._effects
