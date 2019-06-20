from models.battle.battle_model import BattleModel
from models.game_state_model import GameStateModel
from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons
from toolbox.game import Game
from toolbox.singleton import Singleton


class MainMenuController(metaclass=Singleton):
    """Manages the main menu."""

    def show_menu(self) -> None:
        """Show the main menu of the game."""

        from views.main_menu.main_menu_scene import MainMenuScene
        MainMenuScene(self)

    def continue_game(self) -> None:
        """Load the game state and continue the saved game."""

        from controllers.battle_controller import BattleController
        Game().game_state.start_time()
        opponent_pokemons = [PokemonModel(pokemons["BULBASAUR"], pokemons["BULBASAUR"].name, 1,
                                          [LearnedMoveModel(moves["VINE_WHIP"], moves["VINE_WHIP"].default_pp,
                                                            moves["VINE_WHIP"].default_pp),
                                           LearnedMoveModel(moves["GROWL"], moves["GROWL"].default_pp,
                                                            moves["GROWL"].default_pp)])]
        BattleController().battle(BattleModel(opponent_pokemons, "meadow"))

    def new_game(self) -> None:
        """Start a new game."""

        from controllers.map_controller import MapController
        game = Game()
        game.game_state = GameStateModel()
        game.game_state.player.pokemons.append(PokemonModel(pokemons["PIKACHU"], pokemons["PIKACHU"].name, 50, [
            LearnedMoveModel(moves["TAIL_WHIP"]),
            LearnedMoveModel(moves["TAIL_WHIP"]),
            LearnedMoveModel(moves["TAIL_WHIP"]),
            LearnedMoveModel(moves["THUNDER_SHOCK"]),
        ]))
        game.game_state.player.pokemons.append(PokemonModel(pokemons["IVYSAUR"], pokemons["IVYSAUR"].name, 1, [
            LearnedMoveModel(moves["TACKLE"]),
            LearnedMoveModel(moves["GROWL"]),
            LearnedMoveModel(moves["VINE_WHIP"]),
        ]))
        game.game_state.player.pokemons.append(PokemonModel(pokemons["BULBASAUR"], pokemons["BULBASAUR"].name, 5, [
            LearnedMoveModel(moves["TACKLE"], moves["TACKLE"].default_pp, moves["TACKLE"].default_pp),
            LearnedMoveModel(moves["GROWL"], moves["GROWL"].default_pp, moves["GROWL"].default_pp),
            LearnedMoveModel(moves["VINE_WHIP"], moves["VINE_WHIP"].default_pp, moves["VINE_WHIP"].default_pp),
        ]))
        MapController().load_map(game.game_state.map, game.game_state.map_players_position)

    def settings(self) -> None:
        """Set the settings."""

        from controllers.settings_controller import SettingsController
        SettingsController().show_settings()
