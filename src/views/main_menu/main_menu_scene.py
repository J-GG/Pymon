import cocos
from cocos.scenes.transitions import *

from .actions_layer import ActionsLayer
from .background_layer import BackgroundLayer


class MainMenuScene(cocos.scene.Scene):
    """The scene displaying the main menu lets the user to choose between
    starting a new game and continuing an existing one."""

    def __init__(self) -> None:
        """Create the main menu scene."""

        super().__init__()

        self._background = BackgroundLayer()
        self.add(self._background)

        self._actions = ActionsLayer()
        self.add(self._actions)

        cocos.director.director.replace(FadeTransition(self))
