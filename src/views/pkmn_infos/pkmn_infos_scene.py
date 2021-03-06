import typing

import cocos
import pyglet
from cocos.scenes.transitions import *

from controllers.pkmn_infos_controller import PkmnInfosController
from models.battle.battle_model import BattleModel
from models.move_model import MoveModel
from models.pokemon_model import PokemonModel
from toolbox.game import Game
from toolbox.i18n import I18n
from toolbox.init import PATH
from views.common.stat_layer import StatLayer
from views.common.text import Text
from views.pkmn_infos.actions_layer import ActionsLayer
from .action_enum import ActionEnum
from .pkmn_infos_type_enum import PkmnInfosTypeEnum


class PkmnInfosScene(cocos.scene.Scene):
    """Display the information about a Pokemon."""

    def __init__(self, pkmn_infos_controller: PkmnInfosController, pkmn_infos_type: PkmnInfosTypeEnum,
                 pokemon: PokemonModel, selected_action: ActionEnum = None, replace: bool = False,
                 battle: BattleModel = None, new_move: MoveModel = None,
                 cancel_callback: typing.Callable = None) -> None:
        """Create a PKMN infos scene.

        :param pkmn_infos_controller: The controller.
        :param pkmn_infos_type: The type of scene. Affects the information
        displayed and the interactions.
        :param pokemon : The Pokemon the information is to be displayed.
        :param selected_action: The selected action by default.
        :param replace: Whether the scene should replace the previous one or not.
        :param battle: The battle model if it is for a shift.
        :param new_move: The new move to learn if any.
        :param cancel_callback: The function to call if the player chooses to
        cancel.
        """

        super().__init__()

        self._pkmn_infos_controller = pkmn_infos_controller
        self._pkmn_infos_type = pkmn_infos_type
        self._pokemon = pokemon
        self._battle = battle
        self._cancel_callback = cancel_callback

        self._background = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/pkmn_infos/background.jpg'),
                                               anchor=(0, 0))
        self._background.position = (0, 0)
        self.add(self._background)

        self._pokemon_name = cocos.text.Label(pokemon.nickname, bold=True, color=(0, 0, 0, 255), font_size=15)
        self._pokemon_name.position = (
            cocos.director.director.get_window_size()[0] / 2 - self._pokemon_name.element.content_width / 2, 450)
        self.add(self._pokemon_name)

        self._pokemon_types = []
        for type in pokemon.species.type:
            type_sprite = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/types/{0}.png'.format(type.name.lower())),
                anchor=(0, 0))
            type_sprite.scale = 1.5
            self._pokemon_types.append(type_sprite)
            self.add(type_sprite)

        for index, type_sprite in enumerate(self._pokemon_types):
            type_sprite.position = cocos.director.director.get_window_size()[0] / 2 - len(
                self._pokemon_types) * (type_sprite.width + 5) / 2 + index * (type_sprite.width + 5), 420

        self._pokemon_sprite = cocos.sprite.Sprite(
            pyglet.image.load_animation(PATH + '/assets/img/pokemon/front/{0}.gif'.format(pokemon.species.id.lower())))
        self._pokemon_sprite.scale = 1.5
        self._pokemon_sprite.position = (
            cocos.director.director.get_window_size()[0] / 2,
            cocos.director.director.get_window_size()[1] / 2)
        self.add(self._pokemon_sprite)

        self._stats = StatLayer(pokemon, None)
        self._stats.position = (5, 200)
        self.add(self._stats)

        self._experience_background = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/pkmn_infos/experience_background.png'), anchor=(0, 0))
        self._experience_background.opacity = 125
        self._experience_background.position = (0, 90)
        self.add(self._experience_background)
        experience_gained_text = cocos.text.Label(I18n().get("POKEMON_INFOS.EXPERIENCE_POINTS"),
                                                  anchor_x="left", anchor_y="center", bold=True)
        experience_gained_text.position = (
            5, self._experience_background.height / 2 + experience_gained_text.element.content_height / 2 + 2.5)
        self._experience_background.add(experience_gained_text)
        experience_gained = cocos.text.Label(str(pokemon.experience), anchor_x="center", anchor_y="center", bold=True)
        experience_gained.position = (5 + experience_gained_text.element.content_width + (
                self._experience_background.width - experience_gained_text.element.content_width) / 2,
                                      self._experience_background.height / 2 + experience_gained.element.content_height / 2 + 2.5)
        self._experience_background.add(experience_gained)

        experience_next_text = cocos.text.Label(I18n().get("POKEMON_INFOS.NEXT_LEVEL"),
                                                anchor_x="left", anchor_y="center", bold=True)
        experience_next_text.position = (
            5, self._experience_background.height / 2 - experience_next_text.element.content_height / 2 - 2.5)
        self._experience_background.add(experience_next_text)
        experience_next = cocos.text.Label(str(pokemon.experience_for_next_level - pokemon.experience),
                                           anchor_x="center", anchor_y="center", bold=True)
        experience_next.position = (5 + experience_gained_text.element.content_width + (
                self._experience_background.width - experience_gained_text.element.content_width) / 2,
                                    self._experience_background.height / 2 - experience_next.element.content_height / 2 - 2.5)
        self._experience_background.add(experience_next)

        self._level = Text(str(pokemon.level))
        self._level.scale = 1.5

        level_sprite = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/battle/hud/level.png'))
        level_sprite.scale = 2
        level_sprite.position = (
            cocos.director.director.get_window_size()[0] / 2 - level_sprite.width / 2 - self._level.width / 2, 150)
        self.add(level_sprite)

        self._level.position = (
            cocos.director.director.get_window_size()[0] / 2 + level_sprite.width / 2 - self._level.width / 2, 152)
        self.add(self._level)

        self._actions = ActionsLayer(pkmn_infos_type, pokemon, selected_action, battle, new_move)
        self.add(self._actions)

        if replace:
            cocos.director.director.replace(FadeTransition(self))
        else:
            cocos.director.director.push(FadeTransition(self))

    def cancel(self, *args) -> None:
        """Return to the previous scene.

        :param args: The arguments to send to the callback function.
        """

        last_scene = cocos.director.director.scene_stack[len(cocos.director.director.scene_stack) - 1]
        cocos.director.director.pop()
        cocos.director.director.replace(FadeTransition(last_scene))

        if self._cancel_callback:
            self._cancel_callback(*args)

    def next_previous_pokemon(self, selected_action: ActionEnum) -> None:
        """Show the previous or next pokemon."""
        pokemon_index = Game().game_state.player.pokemons.index(
            self._pokemon) - 1 if selected_action == ActionEnum.PREVIOUS else Game().game_state.player.pokemons.index(
            self._pokemon) + 1

        self._pkmn_infos_controller.show_pkmn_infos(pkmn_infos_type=self._pkmn_infos_type,
                                                    pokemon=Game().game_state.player.pokemons[pokemon_index],
                                                    selected_action=selected_action,
                                                    replace=True,
                                                    battle=self._battle,
                                                    new_move=None,
                                                    cancel_callback=self._cancel_callback)

    def shift(self, pokemon: PokemonModel) -> None:
        """Return to the battle scene and shift the current pokemon with the
        specified one.

        :param pokemon: The pokemon to be sent to the battle field.
        """

        last_scene = cocos.director.director.scene_stack[len(cocos.director.director.scene_stack) - 1]
        cocos.director.director.pop()
        cocos.director.director.replace(FadeTransition(last_scene))

        round = True if self._pkmn_infos_type == PkmnInfosTypeEnum.SHIFT else False

        self._pkmn_infos_controller.shift(pokemon, round)
