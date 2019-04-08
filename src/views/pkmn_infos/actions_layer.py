import cocos
import pyglet
from pyglet.window import key as keys

from models.battle.battle_model import BattleModel
from models.pokemon_model import PokemonModel
from toolbox.game import Game
from toolbox.i18n import I18n
from toolbox.init import PATH
from views.common.layer import Layer
from views.pkmn_infos.action_enum import ActionEnum
from .pkmn_infos_type_enum import PkmnInfosTypeEnum


class ActionsLayer(Layer):
    """Shows the list of actions available to the player."""

    SELECTED_SPRITE = "SELECTED_SPRITE"

    is_event_handler = True

    def __init__(self, pkmn_infos_type: PkmnInfosTypeEnum, pokemon: PokemonModel, battle: BattleModel = None) -> None:
        """Create a layer with the list of actions and manage their interaction.

        :param pkmn_infos_type: The type of scene. Affects the information
        displayed and the interactions.
        :param pokemon: The pokemon whose infos is shown.
        :param battle: The battle model if it is for a shift.
        """

        super().__init__()

        self._pokemon = pokemon
        self._available_actions = pkmn_infos_type.value.copy()
        if ActionEnum.SHIFT in self._available_actions and (
                (battle is not None and battle.players_pokemon == pokemon) or pokemon.hp <= 0):
            self._available_actions.remove(ActionEnum.SHIFT)
        if ActionEnum.PREVIOUS in self._available_actions and Game().game_state.player.pokemons.index(pokemon) == 0:
            self._available_actions.remove(ActionEnum.PREVIOUS)
        if ActionEnum.NEXT and Game().game_state.player.pokemons.index(pokemon) == len(
                Game().game_state.player.pokemons) - 1:
            self._available_actions.remove(ActionEnum.NEXT)

        self._selected_action = self._available_actions.index(ActionEnum.CANCEL)
        self._actions = {}

        if ActionEnum.PREVIOUS in self._available_actions:
            previous = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/buttons/small_left.png'), anchor=(0, 0))
            selected_previous = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_left.png'), anchor=(0, 0))
            selected_previous.visible = False
            previous.add(selected_previous, name=ActionsLayer.SELECTED_SPRITE)
            previous_text = cocos.text.Label(I18n().get("POKEMON_INFOS.PREVIOUS"), font_size=20)
            previous_text.position = (previous.width / 2 - previous_text.element.content_width / 1.5,
                                      previous.height / 2 - previous_text.element.content_height / 4)
            previous.add(previous_text)
            self.add(previous)
            self._actions[ActionEnum.PREVIOUS] = previous

        if ActionEnum.SHIFT in self._available_actions:
            shift = cocos.sprite.Sprite(pyglet.image.load(
                PATH + '/assets/img/common/buttons/small_center_red.png'),
                anchor=(0, 0))
            shift.position = (cocos.director.director.get_window_size()[0] / 2 - shift.width - 5, 0)
            selected_shift = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_center_red.png'), anchor=(0, 0))
            selected_shift.visible = False
            shift.add(selected_shift, name=ActionsLayer.SELECTED_SPRITE)
            shift_text = cocos.text.Label(I18n().get("POKEMON_INFOS.SHIFT"), font_size=14)
            shift_text.position = (shift.width / 2 - shift_text.element.content_width / 2,
                                   shift.height / 2 - shift_text.element.content_height / 4)
            shift.add(shift_text)
            self.add(shift)
            self._actions[ActionEnum.SHIFT] = shift

        if ActionEnum.CANCEL in pkmn_infos_type.value:
            cancel = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/common/buttons/small_center.png'),
                                         anchor=(0, 0))
            cancel_position_x = cocos.director.director.get_window_size()[0] / 2
            if ActionEnum.SHIFT not in self._available_actions:
                cancel_position_x -= cancel.width / 2
            cancel.position = (cancel_position_x, 0)
            selected_cancel = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_center.png'), anchor=(0, 0))
            cancel.add(selected_cancel, name=ActionsLayer.SELECTED_SPRITE)
            cancel_text = cocos.text.Label(I18n().get("POKEMON_INFOS.CANCEL"), font_size=14)
            cancel_text.position = (cancel.width / 2 - cancel_text.element.content_width / 2,
                                    cancel.height / 2 - cancel_text.element.content_height / 4)
            cancel.add(cancel_text)
            self.add(cancel)
            self._actions[ActionEnum.CANCEL] = cancel

        if ActionEnum.NEXT in self._available_actions:
            next = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/buttons/small_right.png'), anchor=(0, 0))
            next.position = (cocos.director.director.get_window_size()[0] - next.width, -2)
            selected_next = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_right.png'), anchor=(0, 0))
            selected_next.visible = False
            next.add(selected_next, name=ActionsLayer.SELECTED_SPRITE)
            next_text = cocos.text.Label(I18n().get("POKEMON_INFOS.NEXT"), font_size=20)
            next_text.position = (next.width / 2 - next_text.element.content_width / 4,
                                  next.height / 2 - next_text.element.content_height / 4)
            next.add(next_text)
            self.add(next)
            self._actions[ActionEnum.NEXT] = next

    def _update_screen(self) -> None:
        """update the selected action."""

        for index, action in enumerate(self._available_actions):
            if self._selected_action == index:
                self._actions[action].get(ActionsLayer.SELECTED_SPRITE).visible = True
            else:
                self._actions[action].get(ActionsLayer.SELECTED_SPRITE).visible = False

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected action when pressing UP or BOTTOM.
        Activate the selected action when pressing ENTER.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False
        if key == keys.LEFT and self._selected_action > 0:
            self._selected_action = self._selected_action - 1
            event_handled = True
        elif key == keys.RIGHT and self._selected_action < len(self._available_actions) - 1:
            self._selected_action = self._selected_action + 1
            event_handled = True
        elif key == keys.ENTER:
            if self._available_actions[self._selected_action] == ActionEnum.CANCEL:
                self.parent.cancel()
                event_handled = True
            elif self._available_actions[self._selected_action] == ActionEnum.PREVIOUS:
                self.parent.previous()
                event_handled = True
            elif self._available_actions[self._selected_action] == ActionEnum.NEXT:
                self.parent.next()
                event_handled = True
            elif self._available_actions[self._selected_action] == ActionEnum.SHIFT:
                self.parent.shift(self._pokemon)
                event_handled = True
        elif key == keys.B:
            self.parent.cancel()
            event_handled = True

        self._update_screen()

        return event_handled
