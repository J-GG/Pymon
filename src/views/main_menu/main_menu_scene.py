import typing

import cocos
from cocos.scenes.transitions import *

from controllers.main_menu_controller import MainMenuController
from models.game_state_model import GameStateModel
from .actions_layer import ActionsLayer
from .background_layer import BackgroundLayer


class MainMenuScene(cocos.scene.Scene):
    """The scene displaying the main menu lets the user to choose between
    starting a new game, continuing an existing one and modifying the
    settings."""

    def __init__(self, main_menu_controller: MainMenuController,
                 game_state: typing.Union[None, GameStateModel]) -> None:
        """Create the main menu scene.

        :param game_state: The game state of the saved game if any.
        """

        super().__init__()
        self._main_menu_controller = main_menu_controller

        self._background = BackgroundLayer()
        self.add(self._background)

        self._actions = ActionsLayer(game_state)
        self.add(self._actions)

        cocos.director.director.replace(FadeTransition(self))

    def continue_game(self, game_state: typing.Union[None, GameStateModel]) -> None:
        """Load the game state and continue the saved game.

       :param game_state: The game state of the saved game.
       """

        self._main_menu_controller.continue_game(game_state)

    def new_game(self) -> None:
        """Start a new game."""

        self._main_menu_controller.new_game()
