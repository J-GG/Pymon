from models.learned_move import LearnedMove
from models.pokemon import Pokemon
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons
from views.battle.battle import BattleScene


class BattleController:
    """Manages the battle."""

    @staticmethod
    def battle():
        players_pokemon = Pokemon(pokemons["BULBASAUR"], "Bulbi", 5, [
            LearnedMove(moves["VINE_WHIP"], moves["VINE_WHIP"].default_pp, moves["VINE_WHIP"].default_pp),
            LearnedMove(moves["POISON_POWDER"], moves["POISON_POWDER"].default_pp, moves["POISON_POWDER"].default_pp),
            LearnedMove(moves["GROWL"], moves["GROWL"].default_pp, moves["GROWL"].default_pp),
            LearnedMove(moves["TACKLE"], moves["TACKLE"].default_pp, moves["TACKLE"].default_pp)
        ])
        players_pokemon.current_stats["HP"] = 4
        opponents_pokemon = Pokemon(pokemons["IVYSAUR"], pokemons["IVYSAUR"].name, 10, [moves["VINE_WHIP"]])
        BattleScene(players_pokemon, opponents_pokemon)

    @staticmethod
    def run():
        from controllers.main_menu import MainMenuController
        MainMenuController().show_menu()
