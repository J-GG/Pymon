import random

from models.learned_move import LearnedMove
from models.pokemon import Pokemon
from models.stat_enum import StatEnum
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons
from toolbox.singleton import Singleton
from views.battle.battle import BattleScene


class BattleController(metaclass=Singleton):
    """Manages the battle."""

    def battle(self):
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

    def run(self):
        """The player attempts to escape the battle."""

        from controllers.main_menu import MainMenuController
        MainMenuController().show_menu()

    def uses_move(self, players_pokemon, opponent_pokemon, players_move):
        if players_move.current_pp == 0:
            print("Can't choose this move")

        players_move_effects = players_move.move.effects(players_pokemon, opponent_pokemon)

        for stat, value in players_move_effects["STATS"].items():
            opponent_pokemon.current_stats[stat] = opponent_pokemon.current_stats[stat] + value

        players_move.current_pp = players_move.current_pp - 1 if players_move.current_pp > 0 else 0

        player_attacker = {"pokemon": players_pokemon, "move": players_move, "effects": players_move_effects}
        opponent_attacker = {"pokemon": opponent_pokemon, "move": random.choice(opponent_pokemon.moves),"effects": []}
        if players_pokemon.current_stats[StatEnum.SPEED.name] > opponent_pokemon.current_stats[StatEnum.SPEED.name]:
            first_attacker, second_attacker = player_attacker, opponent_attacker
        else:
            first_attacker, second_attacker = opponent_attacker, player_attacker

        self._battle.round(first_attacker, second_attacker)
