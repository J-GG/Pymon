import random

from models.learned_move import LearnedMove
from models.pokemon import Pokemon
from models.staged_stat_enum import StagedStatEnum
from models.stat_enum import StatEnum
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons
from toolbox.singleton import Singleton
from views.battle.battle import BattleScene


class BattleController(metaclass=Singleton):
    """Manages the battle."""

    def battle(self) -> None:
        """Starts a battle."""
        players_pokemon = Pokemon(pokemons["PIKACHU"], pokemons["PIKACHU"].name, 5, [
            LearnedMove(moves["TAIL_WHIP"], moves["TAIL_WHIP"].default_pp, moves["TAIL_WHIP"].default_pp),
            LearnedMove(moves["THUNDER_SHOCK"], moves["THUNDER_SHOCK"].default_pp, moves["THUNDER_SHOCK"].default_pp),
            LearnedMove(moves["GROWL"], moves["GROWL"].default_pp, moves["GROWL"].default_pp),
        ])
        opponent_pokemon = Pokemon(pokemons["BULBASAUR"], pokemons["BULBASAUR"].name, 5,
                                   [LearnedMove(moves["VINE_WHIP"], moves["VINE_WHIP"].default_pp,
                                                moves["VINE_WHIP"].default_pp),
                                    LearnedMove(moves["GROWL"], moves["GROWL"].default_pp, moves["GROWL"].default_pp)])

        self._battle = BattleScene(players_pokemon, opponent_pokemon)

    def run(self) -> None:
        """The player attempts to escape the battle."""

        from controllers.main_menu import MainMenuController
        MainMenuController().show_menu()

    def uses_move(self, players_pokemon: Pokemon, opponent_pokemon: Pokemon, players_move: LearnedMove) -> None:
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
