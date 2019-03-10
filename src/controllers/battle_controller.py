import typing

from controllers.main_menu_controller import MainMenuController
from models.battle.fight_action_model import FightActionModel
from models.battle.run_action_model import RunActionModel
from models.enumerations.staged_stat_enum import StagedStatEnum
from models.enumerations.stat_enum import StatEnum
from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons
from toolbox.game import Game
from toolbox.singleton import Singleton
from views.battle.battle_scene import BattleScene


class BattleController(metaclass=Singleton):
    """Manages the battle."""

    def battle(self) -> None:
        """Starts a battle."""

        players_pokemon = Game.game_state.player.pokemons[0]
        opponent_pokemon = PokemonModel(pokemons["BULBASAUR"], pokemons["BULBASAUR"].name, 5,
                                        [LearnedMoveModel(moves["VINE_WHIP"], moves["VINE_WHIP"].default_pp,
                                                          moves["VINE_WHIP"].default_pp),
                                         LearnedMoveModel(moves["GROWL"], moves["GROWL"].default_pp,
                                                          moves["GROWL"].default_pp)])

        self._battle = BattleScene(self, players_pokemon, opponent_pokemon)

    def round(self, players_pokemon: PokemonModel, opponent_pokemon: PokemonModel,
              players_action: typing.Union[FightActionModel, RunActionModel]) -> None:
        """Plays the round of the battle.

        :param players_pokemon: The player's pokemon.
        :param opponent_pokemon: The opponent pokemon.
        :param players_action: The action chosen by the player.
        """

        opponent_action = FightActionModel(opponent_pokemon, players_pokemon, opponent_pokemon.moves[0])

        if isinstance(players_action, RunActionModel):
            first_action, second_action = players_action, opponent_action
        else:
            player_speed = players_pokemon.stats[StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
                players_pokemon.staged_stats[StagedStatEnum.SPEED])
            opponent_speed = opponent_pokemon.stats[StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
                opponent_pokemon.staged_stats[StagedStatEnum.SPEED])
            if player_speed > opponent_speed:
                first_action, second_action = players_action, opponent_action
            else:
                first_action, second_action = opponent_action, players_action

        if isinstance(first_action, FightActionModel):
            self._fight_action(first_action)

        if isinstance(second_action, FightActionModel) and second_action.attacker.hp > 0:
            self._fight_action(second_action)

        self._battle.round(first_action, second_action)

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

    def pokemon_ko(self, pokemon_ko: PokemonModel, players_pokemon: PokemonModel,
                   opponent_pokemon: PokemonModel) -> None:
        """A pokemon got defeated.

        The player's pokemon gains some XP if he is the one who won.

        :param pokemon_ko: The pokemon who is KO.
        :param players_pokemon: The player's pokemon.
        :param opponent_pokemon: The opponent pokemon.
        """

        if pokemon_ko == players_pokemon:
            if Game.game_state.player.has_conscious_pokemon:
                self._battle.player_lost_battle()
        else:
            wild_pokemon = 1
            experience_gained = (wild_pokemon * pokemon_ko.species.base_experience * pokemon_ko.level) // 7
            gained_levels = players_pokemon.gain_experience(experience_gained)
            self._battle.player_won_fight(experience_gained, gained_levels)

    def run(self) -> None:
        """The player escapes the battle."""

        MainMenuController().show_menu()

    def lost_battle(self):
        """The player lost the battle. His game state is erased."""

        Game.delete()
        MainMenuController().show_menu()

    def won_battle(self):
        """The player won the battle. His game state is saved."""

        Game.save()
        MainMenuController().show_menu()
