import random

from models.enumerations.staged_stat_enum import StagedStatEnum
from models.enumerations.stat_enum import StatEnum
from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons
from toolbox.singleton import Singleton
from views.battle.battle_scene import BattleScene


class BattleController(metaclass=Singleton):
    """Manages the battle."""

    def battle(self) -> None:
        """Starts a battle."""
        players_pokemon = PokemonModel(pokemons["PIKACHU"], pokemons["PIKACHU"].name, 5, [
            LearnedMoveModel(moves["TAIL_WHIP"], moves["TAIL_WHIP"].default_pp, moves["TAIL_WHIP"].default_pp),
            LearnedMoveModel(moves["THUNDER_SHOCK"], moves["THUNDER_SHOCK"].default_pp,
                             moves["THUNDER_SHOCK"].default_pp),
            LearnedMoveModel(moves["GROWL"], moves["GROWL"].default_pp, moves["GROWL"].default_pp),
        ])
        opponent_pokemon = PokemonModel(pokemons["BULBASAUR"], pokemons["BULBASAUR"].name, 5,
                                        [LearnedMoveModel(moves["VINE_WHIP"], moves["VINE_WHIP"].default_pp,
                                                          moves["VINE_WHIP"].default_pp),
                                         LearnedMoveModel(moves["GROWL"], moves["GROWL"].default_pp,
                                                          moves["GROWL"].default_pp)])

        self._battle = BattleScene(self, players_pokemon, opponent_pokemon)

    def attempt_run(self, players_pokemon: PokemonModel, opponent_pokemon: PokemonModel) -> None:
        """The player attempts to escape the battle.

        :param players_pokemon: The player's pokemon.
        :param opponent_pokemon: The opponent pokemon.
        """

        F = ((players_pokemon.stats[StatEnum.SPEED] * 128) / opponent_pokemon.stats[StatEnum.SPEED] + 30) % 256

        if F > random.randint(0, 255):
            self._battle.successful_run()
        else:
            self._battle.failed_run()

    def run(self) -> None:
        """the player escapes the battle."""

        from controllers.main_menu_controller import MainMenuController
        MainMenuController().show_menu()

    def uses_move(self, players_pokemon: PokemonModel, opponent_pokemon: PokemonModel,
                  players_move: LearnedMoveModel) -> None:
        """The player's pokemon uses the specified learned move on the opponent
         pokemon.

        Determines the effects of the move before transmitting them to the
        view.

        :param players_pokemon: The player's pokemon using the move.
        :param opponent_pokemon: The opponent pokemon on which the move is
        used.
        :param players_move: The move used by the player's pokemon.
        """

        if players_move.current_pp == 0:
            print("Can't choose this move")

        players_used_move_effects = players_move.move.effects(players_pokemon, opponent_pokemon)

        opponent_pokemon.hp = opponent_pokemon.hp + players_used_move_effects.hp

        for staged_stat, value in players_used_move_effects.staged_stats.items():
            if value > 0:
                players_pokemon.staged_stats[staged_stat] = min(6, players_pokemon.staged_stats[staged_stat] + value)
            elif value < 0:
                opponent_pokemon.staged_stats[staged_stat] = max(-6, players_pokemon.staged_stats[staged_stat] + value)

        players_move.current_pp = players_move.current_pp - 1 if players_move.current_pp > 0 else 0

        player_attacker = {"pokemon": players_pokemon, "move": players_move, "effects": players_used_move_effects}
        opponent_attacker = {"pokemon": opponent_pokemon, "move": random.choice(opponent_pokemon.moves), "effects": []}
        player_speed = players_pokemon.stats[StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
            players_pokemon.staged_stats[StagedStatEnum.SPEED])
        opponent_speed = opponent_pokemon.stats[StatEnum.SPEED] * StagedStatEnum.SPEED.get_multiplier(
            opponent_pokemon.staged_stats[StagedStatEnum.SPEED])
        if player_speed > opponent_speed:
            first_attacker, second_attacker = player_attacker, opponent_attacker
        else:
            first_attacker, second_attacker = opponent_attacker, player_attacker

        self._battle.round(first_attacker, second_attacker)
