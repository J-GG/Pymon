import cocos
import pyglet
from pyglet.window import key as keys

from models.pokemon_model import PokemonModel
from toolbox.game import Game
from toolbox.i18n import I18n
from toolbox.init import PATH
from views.common.layer import Layer
from views.pkmn_infos.action_enum import ActionEnum


class ActionsLayer(Layer):
    """Shows the list of actions available to the player."""

    SELECTED_SPRITE = "SELECTED_SPRITE"

    is_event_handler = True

    def __init__(self, pokemon: PokemonModel, action: ActionEnum = ActionEnum.CANCEL) -> None:
        """Create a layer with the list of actions and manage their interaction.

        :param pokemon: The pokemon whose infos is shown.
        :param action: The selected action by default.
        """

        super().__init__()

        self._selected_action = action
        self._actions = []

        self._has_previous = True if Game().game_state.player.pokemons.index(pokemon) != 0 else False
        previous = cocos.sprite.Sprite(
            pyglet.image.load(
                PATH + '/assets/img/common/buttons/{0}small_left.png'.format(
                    "" if self._has_previous else "disabled_")),
            anchor=(0, 0))
        selected_previous = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_left.png'), anchor=(0, 0))
        selected_previous.visible = True if action == ActionEnum.PREVIOUS else False
        previous.add(selected_previous, name=ActionsLayer.SELECTED_SPRITE)
        previous_text = cocos.text.Label(I18n().get("POKEMON_INFOS.PREVIOUS"), font_size=20,
                                         color=(255, 255, 255, 255) if self._has_previous else (125, 125, 125, 255))
        previous_text.position = (previous.width / 2 - previous_text.element.content_width / 1.5,
                                  previous.height / 2 - previous_text.element.content_height / 4)
        previous.add(previous_text)
        self.add(previous)
        self._actions.append(previous)

        cancel = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/common/buttons/small_center.png'),
                                     anchor=(0, 0))
        cancel.position = (cocos.director.director.get_window_size()[0] / 2 - cancel.width / 2, 0)
        selected_cancel = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_center.png'), anchor=(0, 0))
        selected_cancel.visible = True if action == ActionEnum.CANCEL else False
        cancel.add(selected_cancel, name=ActionsLayer.SELECTED_SPRITE)
        cancel_text = cocos.text.Label(I18n().get("POKEMON_INFOS.CANCEL"), font_size=14)
        cancel_text.position = (cancel.width / 2 - cancel_text.element.content_width / 2,
                                cancel.height / 2 - cancel_text.element.content_height / 4)
        cancel.add(cancel_text)
        self.add(cancel)
        self._actions.append(cancel)

        self._has_next = True if Game().game_state.player.pokemons.index(pokemon) != len(
            Game().game_state.player.pokemons) - 1 else False
        next = cocos.sprite.Sprite(
            pyglet.image.load(
                PATH + '/assets/img/common/buttons/{0}small_right.png'.format("" if self._has_next else "disabled_")),
            anchor=(0, 0))
        next.position = (cocos.director.director.get_window_size()[0] - next.width, -2)
        selected_next = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_right.png'), anchor=(0, 0))
        selected_next.visible = True if action == ActionEnum.NEXT else False
        next.add(selected_next, name=ActionsLayer.SELECTED_SPRITE)
        next_text = cocos.text.Label(I18n().get("POKEMON_INFOS.NEXT"), font_size=20,
                                     color=(255, 255, 255, 255) if self._has_next else (125, 125, 125, 255))
        next_text.position = (next.width / 2 - next_text.element.content_width / 4,
                              next.height / 2 - next_text.element.content_height / 4)
        next.add(next_text)
        self.add(next)
        self._actions.append(next)

    def _update_screen(self) -> None:
        """update the selected action."""

        for i in range(len(ActionEnum)):
            if self._selected_action.value == i:
                self._actions[i].get(ActionsLayer.SELECTED_SPRITE).visible = True
            else:
                self._actions[i].get(ActionsLayer.SELECTED_SPRITE).visible = False

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected action when pressing UP or BOTTOM.
        Activate the selected action when pressing ENTER.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False
        if key == keys.LEFT and (
                self._selected_action.value > 1 or (self._has_previous and self._selected_action.value > 0)):
            self._selected_action = ActionEnum(self._selected_action.value - 1)
            event_handled = True
        elif key == keys.RIGHT and (self._selected_action.value < len(ActionEnum) - 2 or
                                    (self._has_next and self._selected_action.value < len(ActionEnum) - 1)):
            self._selected_action = ActionEnum(self._selected_action.value + 1)
            event_handled = True
        elif key == keys.ENTER:
            if self._selected_action == ActionEnum.CANCEL:
                self.parent.cancel()
                event_handled = True
            elif self._selected_action == ActionEnum.PREVIOUS:
                self.parent.previous()
                event_handled = True
            elif self._selected_action == ActionEnum.NEXT:
                self.parent.next()
                event_handled = True
        elif key == keys.B:
            self.parent.cancel()
            event_handled = True

        self._update_screen()

        return event_handled
