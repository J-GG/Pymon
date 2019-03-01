import cocos
import pyglet


class OpponentPokemon(cocos.layer.Layer):
    """The opponent pokemon"""

    def __init__(self):
        super().__init__()

        self._pokemon = cocos.sprite.Sprite(
            pyglet.image.load_animation('../assets/img/pokemon/front/{0}.gif'.format("bulbasaur")))
        self.add(self._pokemon)
