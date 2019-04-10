import typing

from models.battle.battle_model import BattleModel
from models.battle.shift_action_model import ShiftActionModel
from models.pokemon_model import PokemonModel
from toolbox.singleton import Singleton
from views.pkmn_infos.pkmn_infos_type_enum import PkmnInfosTypeEnum


class PkmnInfosController(metaclass=Singleton):
    """Manages the PKMN information."""

    def show_pkmn_infos(self, pkmn_infos_type: PkmnInfosTypeEnum, pokemon: PokemonModel, replace: bool = False,
                        battle: BattleModel = None, cancel_callback: typing.Callable = None) -> None:
        """Show the PKMN information scene.

        :param pkmn_infos_type: The type of scene. Affects the information
        displayed and the interactions.
        :param pokemon: The pokemon the information must be displayed.
        :param replace: Whether to replace or not the scene.
        :param battle: The battle model if it is for a shift.
        :param cancel_callback: The function to call if the player chooses to
        cancel.
        """

        from views.pkmn_infos.pkmn_infos_scene import PkmnInfosScene
        PkmnInfosScene(self, pkmn_infos_type, pokemon, replace, battle, cancel_callback)

    def shift(self, pokemon: PokemonModel, round: bool = True) -> None:
        """Shift the current pokemon with the specified one.

        :param pokemon: The pokemon to be sent to the battle field.
        :param round: Whether the shift is during a round or not.
        """

        from controllers.battle_controller import BattleController

        if round:
            BattleController().round(ShiftActionModel(pokemon))
        else:
            BattleController().shift_players_pokemon(ShiftActionModel(pokemon))
