from models.pokemon_model import PokemonModel
from toolbox.singleton import Singleton
from views.pkmn_infos.pkmn_infos_scene import PkmnInfosScene


class PkmnInfosController(metaclass=Singleton):
    """Manages the PKMN information."""

    def show_pkmn_infos(self, pokemon: PokemonModel) -> None:
        """Show the PKMN information scene.

        :param pokemon: The pokemon the information must be displayed.
        """

        PkmnInfosScene(pokemon)
