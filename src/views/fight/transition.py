import cocos
import pyglet

from toolbox.layer import Layer


class Transition(Layer):
    """The transition played just before the beginning of the fight."""

    def __init__(self):
        super(Transition, self).__init__()

        self._background = cocos.sprite.Sprite(pyglet.image.load_animation('../assets/fight/battle_transition.gif'))
        self._background.scale = 1.5
        self._background.position = (
            cocos.director.director.get_window_size()[0] / 2,
            cocos.director.director.get_window_size()[1] / 2
        )
        self.add(self._background)
