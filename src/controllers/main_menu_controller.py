import typing

from models.game_state_model import GameStateModel
from toolbox.game import Game
from toolbox.singleton import Singleton


class MainMenuController(metaclass=Singleton):
    """Manages the main menu."""

    def show_menu(self) -> None:
        """Show the main menu of the game."""

        from views.main_menu.main_menu_scene import MainMenuScene
        saved_game_state = Game.load()
        MainMenuScene(self, saved_game_state)

    def continue_game(self, game_state: typing.Union[None, GameStateModel]) -> None:
        """Load the game state and continue the saved game.

       :param game_state: The game state of the saved game.
       """

        from controllers.battle_controller import BattleController
        game_state.start_time()
        Game.set_game_state(game_state)
        BattleController().battle()

    def new_game(self) -> None:
        """Start a new game."""

        from controllers.battle_controller import BattleController
        game_state = GameStateModel()
        game_state.start_time()
        Game.set_game_state(game_state)
        BattleController().battle()
