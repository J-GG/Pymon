import cocos
import pyglet

from models.pokemon import Pokemon
from toolbox.init import PATH


class OpponentPokemon(cocos.layer.Layer):
    """The opponent pokemon"""

    def __init__(self, opponent_pokemon: Pokemon) -> None:
        """Create a new layer showing the opponent pokemon.

        :param opponent_pokemon: The opponent pokemon.
        """

        super().__init__()

        self._pokemon = cocos.sprite.Sprite(
            pyglet.image.load_animation(
                PATH + '/assets/img/pokemon/front/{0}.gif'.format(opponent_pokemon.species.name)))
        self.add(self._pokemon)
