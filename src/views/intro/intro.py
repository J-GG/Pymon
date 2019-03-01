import cocos
from cocos.actions import *

from controllers.main_menu import MainMenuController
from .background import Background


class IntroScene(cocos.scene.Scene):
    """The scene displaying the introduction of the game."""

    def __init__(self):
        super(IntroScene, self).__init__()

        self._background = Background()
        self.add(self._background)

        self.do(Delay(0.1) + CallFunc(MainMenuController().show_menu))

        cocos.director.director.run(self)
