import cocos
import pyglet

from models.pokemon import Pokemon as PokemonModel
from toolbox.init import PATH


class Pokemon(cocos.layer.Layer):
    """The player's pokemon"""

    def __init__(self, players_pokemon: PokemonModel) -> None:
        """Create a new layer showing the player's pokemon.

        :param players_pokemon: The player's pokemon.
        """

        super().__init__()

        self._pokemon = cocos.sprite.Sprite(
            pyglet.image.load_animation(PATH + '/assets/img/pokemon/back/{0}.gif'.format(players_pokemon.species.name)))
        self.add(self._pokemon)
