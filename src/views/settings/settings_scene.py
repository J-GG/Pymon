import typing

import cocos
from cocos.scenes.transitions import *

from controllers.settings_controller import SettingsController
from models.settings.settings_model import SettingsModel
from .actions_layer import ActionsLayer
from .background_layer import BackgroundLayer


class SettingsScene(cocos.scene.Scene):
    """The scene displaying the settings lets the user to choose the
    language."""

    def __init__(self, settings_controller: SettingsController, settings: SettingsModel) -> None:
        """Create the settings scene.

        :param settings_controller: The settings controller.
        :param settings: The player's settings.
        """

        super().__init__()
        self._settings_controller = settings_controller

        self._background = BackgroundLayer()
        self.add(self._background)

        self._actions = ActionsLayer(settings)
        self.add(self._actions)

        cocos.director.director.replace(FadeTransition(self))

    def cancel_settings(self, new_settings: typing.Dict) -> None:
        """Send the settings to the controller.

        :param new_settings: The new settings set by the player.
        """

        self._settings_controller.cancel_settings(new_settings)
