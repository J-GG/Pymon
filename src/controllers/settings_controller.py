import typing

from models.settings.language_enum import LanguageEnum
from toolbox.game import Game
from toolbox.singleton import Singleton


class SettingsController(metaclass=Singleton):
    """Manages the settings."""

    def show_settings(self) -> None:
        """Show the settings of the game."""

        from views.settings.settings_scene import SettingsScene
        SettingsScene(self, Game().settings)

    def cancel_settings(self, new_settings: typing.Dict) -> None:
        """Save the settings and go back to the main menu.

        :param new_settings: The new settings set by the player.
        """

        from controllers.main_menu_controller import MainMenuController
        if LanguageEnum in new_settings:
            Game().settings.language = new_settings[LanguageEnum]

        Game().settings.save()
        MainMenuController().show_menu()
