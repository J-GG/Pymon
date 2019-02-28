import cocos

from .actions import Actions
from .background import Background


class MainMenuScene(cocos.scene.Scene):
    """The scene displaying the main menu lets the user to choose between
    starting a new game and continuing an existing one."""

    def __init__(self):
        super(MainMenuScene, self).__init__()

        self._background = Background()
        self.add(self._background)

        self._actions = Actions()
        self.add(self._actions)

        cocos.director.director.run(self)
