import cocos
import pyglet

from toolbox.init import PATH


class Pokemon(cocos.layer.Layer):
    """The player's pokemon"""

    def __init__(self):
        super().__init__()

        self._pokemon = cocos.sprite.Sprite(
            pyglet.image.load_animation(PATH + '/assets/img/pokemon/back/{0}.gif'.format("pikachu")))
        self.add(self._pokemon)
