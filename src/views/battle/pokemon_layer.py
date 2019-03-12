import cocos
import pyglet

from models.pokemon_model import PokemonModel
from toolbox.init import PATH


class PokemonLayer(cocos.layer.Layer):
    """The player's pokemon"""

    def __init__(self, players_pokemon: PokemonModel) -> None:
        """Create a new layer showing the player's pokemon.

        :param players_pokemon: The player's pokemon.
        """

        super().__init__()

        self._pokemon = cocos.sprite.Sprite(
            pyglet.image.load_animation(
                PATH + '/assets/img/pokemon/back/{0}.gif'.format(players_pokemon.species.id.lower())))
        self.add(self._pokemon)
