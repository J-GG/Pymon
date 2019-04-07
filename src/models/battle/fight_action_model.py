import random

from models.battle.battle_model import BattleModel
from models.battle.used_move_effects_model import UsedMoveEffectsModel
from models.enumerations.move_category_enum import MoveCategoryEnum
from models.enumerations.staged_stat_enum import StagedStatEnum
from models.enumerations.stat_enum import StatEnum
from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel


class FightActionModel:
    """Represents the use of a move during a battle."""

    def __init__(self, battle: BattleModel, attacker_is_player: bool, move: LearnedMoveModel) -> None:
        """Create a new fight action.

        :param battle: The model containing the data about the battle.
        :param attacker_is_player: Whether the attacker is the player's pokemon.
        :param move: The move used by the attacker against the defender.
        """

        self._battle = battle
        self._attacker_is_player = attacker_is_player
        self._move = move
        self._effects = None

    @property
    def attacker(self) -> PokemonModel:
        """Get the attacking pokemon.

        :return: The ``PokemonModel`` of the attacking pokemon.
        """

        return self._battle.players_pokemon if self._attacker_is_player else self._battle.opponent_pokemon

    @property
    def defender(self) -> PokemonModel:
        """Get the defending pokemon.

        :return: The ``PokemonModel`` of the defending pokemon.
        """

        return self._battle.opponent_pokemon if self._attacker_is_player else self._battle.players_pokemon

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
                self.attacker.staged_stats[StagedStatEnum.ACCURACY]) if self._move.move.accuracy else False
            effectiveness = None
            critical_multiplier = None
            staged_stats = dict()
            damage = 0

            if not failed:
                if self._move.move.category in [MoveCategoryEnum.PHYSICAL, MoveCategoryEnum.SPECIAL]:
                    if self._move.move.category == MoveCategoryEnum.PHYSICAL:
                        attack = self.attacker.stats[StatEnum.ATTACK] * StagedStatEnum.ATTACK.get_multiplier(
                            self.attacker.staged_stats[StagedStatEnum.ATTACK])
                        defense = self.defender.stats[StatEnum.DEFENSE] * StagedStatEnum.DEFENSE.get_multiplier(
                            self.defender.staged_stats[StagedStatEnum.DEFENSE])
                    else:
                        attack = self.attacker.stats[
                                     StatEnum.SPECIAL_ATTACK] * StagedStatEnum.SPECIAL_ATTACK.get_multiplier(
                            self.attacker.staged_stats[StagedStatEnum.SPECIAL_ATTACK])
                        defense = self.defender.stats[
                                      StatEnum.SPECIAL_ATTACK] * StagedStatEnum.SPECIAL_DEFENSE.get_multiplier(
                            self.defender.staged_stats[StagedStatEnum.SPECIAL_DEFENSE])

                    effectiveness = self._move.move.type.effectiveness(self.defender.species.type)
                    critical_multiplier = 1.5 if random.randint(1, 256) <= self.attacker.stats[
                        StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
                        self.attacker.staged_stats[StagedStatEnum.SPEED]) / 2 else 1
                    modifier = critical_multiplier * effectiveness.value * random.uniform(0.85, 1)
                    damage = round(
                        ((
                                 2 * self.attacker.level / 5 + 2) * self._move.move.power * attack / defense / 50 + 5) * modifier)
                    damage = max(1, damage) * -1

                staged_stats = self._move.move.effects.staged_stats if self._move.move.effects else dict()

            self._effects = UsedMoveEffectsModel(failed, damage, staged_stats, effectiveness,
                                                 critical_multiplier == 1.5)

        return self._effects
