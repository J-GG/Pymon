import cocos
import pyglet

from toolbox.init import PATH


class OpponentPokemon(cocos.layer.Layer):
    """The opponent pokemon"""

    def __init__(self, opponent_pokemon):
        super().__init__()

        self._pokemon = cocos.sprite.Sprite(
            pyglet.image.load_animation(
                PATH + '/assets/img/pokemon/front/{0}.gif'.format(opponent_pokemon.species.name)))
        self.add(self._pokemon)
