import cocos
import pyglet
from cocos.scenes.transitions import *

from controllers.pkmn_infos_controller import PkmnInfosController
from models.pokemon_model import PokemonModel
from toolbox.game import Game
from toolbox.i18n import I18n
from toolbox.init import PATH
from views.common.stat_layer import StatLayer
from views.common.text import Text
from views.pkmn_infos.actions_layer import ActionsLayer


class PkmnInfosScene(cocos.scene.Scene):
    """Display the information about a Pokemon."""

    SELECTED_SPRITE = "SELECTED_SPRITE"

    def __init__(self, pkmn_infos_controller: PkmnInfosController, pokemon: PokemonModel,
                 replace: bool = False) -> None:
        """Create a PKMN infos scene.

        :param pkmn_infos_controller: The controller.
        :param pokemon : The Pokemon the information is to be displayed.
        :param replace: Whether the scene should replace the previous one or not.
        """

        super().__init__()

        self._pkmn_infos_controller = pkmn_infos_controller
        self._pokemon = pokemon

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

        self._moves = []
        for index, move in enumerate(pokemon.moves):
            move_sprite = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/battle/moves/{0}.png'.format(move.move.type.name.lower())))
            move_sprite.position = (
                cocos.director.director.get_window_size()[0] - move_sprite.width / 2, 350 - 40 * index)

            selected_sprite = cocos.sprite.Sprite(pyglet.image.load(
                PATH + '/assets/img/battle/moves/selected_{0}.png'.format(move.move.type.name.lower())))
            selected_sprite.visible = False
            move_sprite.add(selected_sprite, name=PkmnInfosScene.SELECTED_SPRITE)

            name = cocos.text.Label(move.move.name, font_size=9, anchor_x="left", anchor_y="center",
                                    color=(0, 0, 0, 255), bold=True)
            name.position = -57, 8
            move_sprite.add(name)

            pp = cocos.text.Label("PP {0}/{1}".format(move.current_pp, move.pp),
                                  font_size=9, anchor_x="left", anchor_y="center", bold=True)
            pp.position = (-15, -8)
            move_sprite.add(pp)

            type = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/types/{0}.png'.format(move.move.type.name.lower())))
            type.position = (-35, -8)
            type.scale = 0.9
            move_sprite.add(type)

            self._moves.append(move_sprite)
            self.add(move_sprite)

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

        self._actions = ActionsLayer(pokemon)
        self.add(self._actions)

        if replace:
            cocos.director.director.replace(FadeTransition(self))
        else:
            cocos.director.director.push(FadeTransition(self))

    def cancel(self) -> None:
        """Return to the previous scene."""

        last_scene = cocos.director.director.scene_stack[len(cocos.director.director.scene_stack) - 1]
        cocos.director.director.pop()
        cocos.director.director.replace(FadeTransition(last_scene))

    def previous(self) -> None:
        """Show the previous pokemon."""

        self._pkmn_infos_controller.show_pkmn_infos(
            Game().game_state.player.pokemons[Game().game_state.player.pokemons.index(self._pokemon) - 1], True)

    def next(self) -> None:
        """Show the next pokemon."""

        self._pkmn_infos_controller.show_pkmn_infos(
            Game().game_state.player.pokemons[Game().game_state.player.pokemons.index(self._pokemon) + 1], True)
