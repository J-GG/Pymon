from models.battle.battle_model import BattleModel
from models.battle.shift_action_model import ShiftActionModel
from models.pokemon_model import PokemonModel
from toolbox.singleton import Singleton
from views.pkmn_infos.pkmn_infos_type_enum import PkmnInfosTypeEnum


class PkmnInfosController(metaclass=Singleton):
    """Manages the PKMN information."""

    def show_pkmn_infos(self, pkmn_infos_type: PkmnInfosTypeEnum, pokemon: PokemonModel, replace: bool = False,
                        battle: BattleModel = None) -> None:
        """Show the PKMN information scene.

        :param pkmn_infos_type: The type of scene. Affects the information
        displayed and the interactions.
        :param pokemon: The pokemon the information must be displayed.
        :param replace: Whether to replace or not the scene.
        :param battle: The battle model if it is for a shift.
        """

        from views.pkmn_infos.pkmn_infos_scene import PkmnInfosScene
        PkmnInfosScene(self, pkmn_infos_type, pokemon, replace, battle)

    def shift(self, pokemon: PokemonModel) -> None:
        """Shift the current pokemon with the specified one.

        :param pokemon: The pokemon to be sent to the battle field.
        """

        from controllers.battle_controller import BattleController
        BattleController().round(ShiftActionModel(pokemon))
