import cocos
from cocos.actions import *

from controllers.main_menu_controller import MainMenuController
from .background_layer import BackgroundLayer


class IntroScene(cocos.scene.Scene):
    """The scene displaying the introduction of the game."""

    def __init__(self) -> None:
        """Create the intro scene."""

        super().__init__()

        self._background = BackgroundLayer()
        self.add(self._background)

        self.do(Delay(0.1) + CallFunc(MainMenuController().show_menu))

        cocos.director.director.run(self)
