import typing

from controllers.main_menu_controller import MainMenuController
from controllers.pkmn_infos_controller import PkmnInfosController
from models.battle.battle_model import BattleModel
from models.battle.fight_action_model import FightActionModel
from models.battle.run_action_model import RunActionModel
from models.enumerations.staged_stat_enum import StagedStatEnum
from models.enumerations.stat_enum import StatEnum
from models.pokemon_model import PokemonModel
from toolbox.game import Game
from toolbox.singleton import Singleton
from views.battle.battle_scene import BattleScene


class BattleController(metaclass=Singleton):
    """Manages the battle."""

    def battle(self, battle: BattleModel) -> None:
        """Starts a battle.

        :param battle: The data of the battle.
        """

        self._battle = battle
        self._battle_scene = BattleScene(self, battle)

    def round(self, players_action: typing.Union[FightActionModel, RunActionModel]) -> None:
        """Plays the round of the battle.

        :param players_action: The action chosen by the player.
        """

        opponent_action = FightActionModel(self._battle.opponent_pokemon, self._battle.players_pokemon,
                                           self._battle.opponent_pokemon.moves[0])

        if isinstance(players_action, RunActionModel):
            first_action, second_action = players_action, opponent_action
        else:
            player_speed = self._battle.players_pokemon.stats[StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
                self._battle.players_pokemon.staged_stats[StagedStatEnum.SPEED])
            opponent_speed = self._battle.opponent_pokemon.stats[StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
                self._battle.opponent_pokemon.staged_stats[StagedStatEnum.SPEED])
            if player_speed > opponent_speed:
                first_action, second_action = players_action, opponent_action
            else:
                first_action, second_action = opponent_action, players_action

        if isinstance(first_action, FightActionModel):
            self._fight_action(first_action)

        if isinstance(second_action, FightActionModel) and second_action.attacker.hp > 0:
            if not isinstance(first_action, RunActionModel) or (
                    isinstance(first_action, RunActionModel) and not first_action.is_run_successful()):
                self._fight_action(second_action)

        self._battle_scene.round(first_action, second_action)

    def _fight_action(self, fight_action: FightActionModel) -> None:
        """A move has been chosen as an action. Apply its effects.

        :param fight_action: The ``FightActionModel`` containing all the
        information about the move.
        """

        move_effects = fight_action.get_effects()

        fight_action.defender.hp = fight_action.defender.hp + move_effects.hp
        if fight_action.defender.hp < 0:
            fight_action.defender.hp = 0
        elif fight_action.defender.hp > fight_action.defender.stats[StatEnum.HP]:
            fight_action.defender.hp = fight_action.defender.stats[StatEnum.HP]

        for staged_stat, value in move_effects.staged_stats.items():
            if value > 0:
                fight_action.attacker.staged_stats[staged_stat] = min(6, fight_action.attacker.staged_stats[
                    staged_stat] + value)
            elif value < 0:
                fight_action.defender.staged_stats[staged_stat] = max(-6, fight_action.defender.staged_stats[
                    staged_stat] + value)

        fight_action.move.current_pp = fight_action.move.current_pp - 1 if fight_action.move.current_pp > 0 else 0

    def pokemon_ko(self, pokemon_ko: PokemonModel) -> None:
        """A pokemon got defeated.

        The player's pokemon gains some XP if he is the one who won.

        :param pokemon_ko: The pokemon who is KO.
        """

        if pokemon_ko == self._battle.players_pokemon:
            if Game().game_state.player.has_conscious_pokemon:
                self._battle_scene.player_lost_battle()
        else:
            wild_pokemon = 1
            experience_gained = (wild_pokemon * pokemon_ko.species.base_experience * pokemon_ko.level) // 7
            gained_levels = self._battle.players_pokemon.gain_experience(experience_gained)
            self._battle_scene.player_won_fight(experience_gained, gained_levels)

    def run(self) -> None:
        """The player escapes the battle."""

        MainMenuController().show_menu()

    def infos_pkmn(self) -> None:
        """Show the PKMN information scene."""

        PkmnInfosController().show_pkmn_infos(self._battle.players_pokemon)

    def lost_battle(self) -> None:
        """The player lost the battle. His game state is erased."""

        Game().game_state.delete()
        MainMenuController().show_menu()

    def won_battle(self) -> None:
        """The player won the battle. His game state is saved."""

        Game().game_state.save()
        MainMenuController().show_menu()
