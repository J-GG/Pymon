from models.game_state_model import GameStateModel
from toolbox.game import Game
from toolbox.singleton import Singleton


class MainMenuController(metaclass=Singleton):
    """Manages the main menu."""

    def show_menu(self) -> None:
        """Show the main menu of the game."""

        from views.main_menu.main_menu_scene import MainMenuScene
        MainMenuScene(self, Game().game_state)

    def continue_game(self) -> None:
        """Load the game state and continue the saved game."""

        from controllers.battle_controller import BattleController
        Game().game_state.start_time()
        BattleController().battle()

    def new_game(self) -> None:
        """Start a new game."""

        from controllers.battle_controller import BattleController
        Game().game_state = GameStateModel()
        BattleController().battle()

    def settings(self) -> None:
        """Set the settings."""

        from controllers.settings_controller import SettingsController
        SettingsController().show_settings()
