import cocos
import pyglet
from pyglet.window import key as keys

from models.battle.battle_model import BattleModel
from models.move_model import MoveModel
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

    def __init__(self, pkmn_infos_type: PkmnInfosTypeEnum, pokemon: PokemonModel, selected_action: ActionEnum = None,
                 battle: BattleModel = None, new_move: MoveModel = None) -> None:
        """Create a layer with the list of actions and manage their interaction.

        :param pkmn_infos_type: The type of scene. Affects the information
        displayed and the interactions.
        :param pokemon: The pokemon whose infos is shown.
        :param selected_action: The selected action by default.
        :param battle: The battle model if it is for a shift.
        :param new_move: The new move to learn if any.
        """

        super().__init__()

        self._pokemon = pokemon
        self._pkmn_infos_type = pkmn_infos_type
        self._new_move = new_move
        self._available_actions = pkmn_infos_type.actions.copy()
        if ActionEnum.SHIFT in self._available_actions and (
                (battle is not None and battle.players_pokemon == pokemon) or pokemon.hp <= 0):
            self._available_actions.remove(ActionEnum.SHIFT)
        if ActionEnum.PREVIOUS in self._available_actions and Game().game_state.player.pokemons.index(pokemon) == 0:
            self._available_actions.remove(ActionEnum.PREVIOUS)
        if ActionEnum.NEXT and Game().game_state.player.pokemons.index(pokemon) == len(
                Game().game_state.player.pokemons) - 1:
            self._available_actions.remove(ActionEnum.NEXT)

        self._selected_action = self._available_actions.index(
            selected_action) if selected_action and selected_action in self._available_actions else self._available_actions.index(
            pkmn_infos_type.default_action)
        self._actions = {}

        if ActionEnum.PREVIOUS in self._available_actions:
            previous = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/buttons/small_left.png'), anchor=(0, 0))
            selected_previous = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/buttons/selected_small_left.png'), anchor=(0, 0))
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
            shift.add(selected_shift, name=ActionsLayer.SELECTED_SPRITE)
            shift_text = cocos.text.Label(I18n().get("POKEMON_INFOS.SHIFT"), font_size=14)
            shift_text.position = (shift.width / 2 - shift_text.element.content_width / 2,
                                   shift.height / 2 - shift_text.element.content_height / 4)
            shift.add(shift_text)
            self.add(shift)
            self._actions[ActionEnum.SHIFT] = shift

        if ActionEnum.CANCEL in self._available_actions:
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
            next.add(selected_next, name=ActionsLayer.SELECTED_SPRITE)
            next_text = cocos.text.Label(I18n().get("POKEMON_INFOS.NEXT"), font_size=20)
            next_text.position = (next.width / 2 - next_text.element.content_width / 4,
                                  next.height / 2 - next_text.element.content_height / 4)
            next.add(next_text)
            self.add(next)
            self._actions[ActionEnum.NEXT] = next

        list_moves = pokemon.moves + [new_move] if new_move else pokemon.moves
        for index, move in enumerate(list_moves):
            name = move.name.capitalize() if isinstance(move, MoveModel) else move.move.name.capitalize()
            current_pp = move.default_pp if isinstance(move, MoveModel) else move.current_pp
            max_pp = move.default_pp if isinstance(move, MoveModel) else move.pp
            type = move.type.name.lower() if isinstance(move, MoveModel) else move.move.type.name.lower()
            y_position = 170 if isinstance(move, MoveModel) else 350 - 40 * index

            move_sprite = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/battle/moves/{0}.png'.format(type)))
            move_sprite.position = (
                cocos.director.director.get_window_size()[0] - move_sprite.width / 2, y_position)

            selected_sprite = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/battle/moves/selected_{0}.png'.format(type)))
            selected_sprite.visible = False
            move_sprite.add(selected_sprite, name=ActionsLayer.SELECTED_SPRITE)

            name_label = cocos.text.Label(name, font_size=9, anchor_x="left", anchor_y="center", color=(0, 0, 0, 255),
                                          bold=True)
            name_label.position = (-57, 8)
            move_sprite.add(name_label)

            pp = cocos.text.Label("PP {0}/{1}".format(current_pp, max_pp),
                                  font_size=9, anchor_x="left", anchor_y="center", bold=True)
            pp.position = (-15, -8)
            move_sprite.add(pp)

            type = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/common/types/{0}.png'.format(type)))
            type.position = (-35, -8)
            type.scale = 0.9
            move_sprite.add(type)

            self.add(move_sprite)
            if pkmn_infos_type == PkmnInfosTypeEnum.NEW_MOVE:
                self._actions[self._available_actions[index]] = move_sprite

        self._update_screen()

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
            self._selected_action -= 1
            event_handled = True
        elif key == keys.RIGHT and self._selected_action < len(self._available_actions) - 1:
            self._selected_action += 1
            event_handled = True
        elif key == keys.UP and self._pkmn_infos_type == PkmnInfosTypeEnum.NEW_MOVE and self._selected_action > 0:
            self._selected_action -= 1
            event_handled = True
        elif key == keys.DOWN and self._pkmn_infos_type == PkmnInfosTypeEnum.NEW_MOVE and self._selected_action < len(
                self._available_actions) - 1:
            self._selected_action += 1
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
            elif self._available_actions[self._selected_action] == ActionEnum.NEW_MOVE:
                self.parent.cancel()
                event_handled = True
            elif self._available_actions[self._selected_action] in [ActionEnum.MOVE_1, ActionEnum.MOVE_2,
                                                                    ActionEnum.MOVE_3, ActionEnum.MOVE_4]:
                self.parent.cancel([self._pokemon.moves[self._selected_action]])
                event_handled = True
        elif key == keys.B:
            self.parent.cancel()
            event_handled = True

        self._update_screen()

        return event_handled
