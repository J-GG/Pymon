import cocos
import pyglet

from models.pokemon_model import PokemonModel
from toolbox.init import PATH


class OpponentPokemonLayer(cocos.layer.Layer):
    """The opponent pokemon"""

    def __init__(self, opponent_pokemon: PokemonModel) -> None:
        """Create a new layer showing the opponent pokemon.

        :param opponent_pokemon: The opponent pokemon.
        """

        super().__init__()

        self._pokemon = cocos.sprite.Sprite(
            pyglet.image.load_animation(
                PATH + '/assets/img/pokemon/front/{0}.gif'.format(opponent_pokemon.species.id.lower())))
        self.add(self._pokemon)
