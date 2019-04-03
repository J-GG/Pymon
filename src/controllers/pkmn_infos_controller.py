from models.pokemon_model import PokemonModel
from toolbox.singleton import Singleton


class PkmnInfosController(metaclass=Singleton):
    """Manages the PKMN information."""

    def show_pkmn_infos(self, pokemon: PokemonModel, replace: bool = False) -> None:
        """Show the PKMN information scene.

        :param pokemon: The pokemon the information must be displayed.
        :param replace: Whether to replace or not the scene.
        """

        from views.pkmn_infos.pkmn_infos_scene import PkmnInfosScene
        PkmnInfosScene(self, pokemon, replace)
