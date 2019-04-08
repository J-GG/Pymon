from models.battle.battle_model import BattleModel
from models.game_state_model import GameStateModel
from toolbox.game import Game
from toolbox.singleton import Singleton
from views.pkmn_infos.pkmn_infos_type_enum import PkmnInfosTypeEnum


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
        BattleController().battle(BattleModel())

    def new_game(self) -> None:
        """Start a new game."""

        Game().game_state = GameStateModel()
        # from controllers.battle_controller import BattleController
        # BattleController().battle(BattleModel())
        from controllers.pkmn_infos_controller import PkmnInfosController
        PkmnInfosController().show_pkmn_infos(PkmnInfosTypeEnum.SHIFT, Game().game_state.player.pokemons[0])

    def settings(self) -> None:
        """Set the settings."""

        from controllers.settings_controller import SettingsController
        SettingsController().show_settings()
