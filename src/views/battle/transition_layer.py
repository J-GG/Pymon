import cocos
import pyglet

from toolbox.init import PATH
from views.common.layer import Layer


class TransitionLayer(Layer):
    """The transition played just before the beginning of the battle."""

    def __init__(self) -> None:
        """Create a new transition layer."""

        super().__init__()

        self._background = cocos.sprite.Sprite(
            pyglet.image.load_animation(PATH + '/assets/img/battle/battle_transition.gif'))
        self._background.scale = 1.5
        self._background.position = (
            cocos.director.director.get_window_size()[0] / 2,
            cocos.director.director.get_window_size()[1] / 2
        )
        self.add(self._background)
