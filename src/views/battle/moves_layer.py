import cocos
import pyglet
from cocos.actions import *

from models.pokemon_model import PokemonModel
from toolbox.i18n import I18n
from toolbox.init import PATH
from toolbox.keyboard import is_key_cancel, is_key_action, is_key_down, is_key_up
from views.common.layer import Layer


class MovesLayer(Layer):
    """Shows the pokemon's list of moves."""

    SELECTED_SPRITE = "SELECTED_SPRITE"

    is_event_handler = True

    def __init__(self, pokemon: PokemonModel) -> None:
        """Show the pokemon's list of moves and ask the player to choose one.

        :param pokemon: The player's pokemon.
        """

        super().__init__()
        self._pokemon = pokemon
        self._selected = 0

        self._is_visible = False
        self._actions = dict()
        self.update_moves()

        self._actions[len(self._actions)] = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/common/buttons/small_right.png'))
        self._actions[len(self._actions) - 1].position = 615 + self._actions[len(self._actions) - 1].width, 90
        self.add(self._actions[len(self._actions) - 1])

        selected_sprite = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_right.png'))
        selected_sprite.visible = False
        self._actions[len(self._actions) - 1].add(selected_sprite, name=MovesLayer.SELECTED_SPRITE)

        text = cocos.text.Label(I18n().get("BATTLE.MOVE_RETURN"), anchor_y="top", font_size=30)
        text.position = (-text.element.content_width / 2 + 3, text.element.content_height / 2 - 2)
        self._actions[len(self._actions) - 1].add(text)

    def _update_selected_action(self) -> None:
        """Show the selected sprite of the selected action."""

        for action in range(len(self._actions)):
            self._actions[action].get(MovesLayer.SELECTED_SPRITE).visible = False

        self._actions[self._selected].get(MovesLayer.SELECTED_SPRITE).visible = True

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected move when pressing UP or BOTTOM.
        Choose the selected move when pressing ENTER or go back to the
        previous menu.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False
        if self._is_visible:
            if is_key_cancel(key) or (is_key_action(key) and self._selected == len(self._actions) - 1):
                self.do(CallFunc(self.toggle_apparition) + Delay(0.3) + CallFunc(self.parent.show_actions))
                event_handled = True
            elif is_key_action(key):
                self.parent.fight_action(self._pokemon.moves[self._selected])
                event_handled = True
            elif is_key_up(key) and self._selected > 0:
                self._selected = self._selected - 1
                event_handled = True
            elif is_key_down(key) and self._selected < len(self._actions) - 1:
                self._selected = self._selected + 1
                event_handled = True

            self._update_selected_action()

            return event_handled

    def toggle_apparition(self) -> None:
        """Show or hide the list of moves."""

        nb_moves = len(self._pokemon.moves)
        for index in range(nb_moves):
            offset = self._actions[index].width if self._is_visible else -self._actions[index].width
            self._actions[index].do(Delay(0.1 * len(self._actions) - (0.1 * index))
                                    + MoveTo((715 + offset, 250 - 40 * index), 0.2))

        return_offset = self._actions[nb_moves].width if self._is_visible else -self._actions[nb_moves].width
        self._actions[nb_moves].do(MoveTo((670 + return_offset, 90), 0.2))

        self._is_visible = not self._is_visible

        if self._is_visible:
            self._selected = 0
            self._update_selected_action()

    def update_moves(self) -> None:
        """Update the list of moves."""

        for index, move in enumerate(self._pokemon.moves):
            if index in self._actions:
                self.remove(self._actions[index])

            self._actions[index] = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/battle/moves/{0}.png'.format(move.move.type.name.lower())))
            offset = 0 if self._is_visible else self._actions[index].width
            self._actions[index].position = 715 + offset, 250 - 40 * index

            selected_sprite = cocos.sprite.Sprite(pyglet.image.load(
                PATH + '/assets/img/battle/moves/selected_{0}.png'.format(move.move.type.name.lower())))
            selected_sprite.visible = False
            self._actions[index].add(selected_sprite, name=MovesLayer.SELECTED_SPRITE)

            name = cocos.text.Label(move.move.name, font_size=9, anchor_x="left", anchor_y="center",
                                    color=(0, 0, 0, 255), bold=True)
            name.position = -57, 8
            self._actions[index].add(name)

            pp = cocos.text.Label("PP {0}/{1}".format(move.current_pp, move.pp),
                                  font_size=9, anchor_x="left", anchor_y="center", bold=True)
            pp.position = (-15, -8)
            self._actions[index].add(pp)
            type = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/types/{0}.png'.format(move.move.type.name.lower())))
            type.position = (-35, -8)
            type.scale = 0.9
            self._actions[index].add(type)

            self.add(self._actions[index])
