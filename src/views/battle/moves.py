import cocos
from cocos.actions import *

from views.common.key_enum import KeyEnum
from views.common.layer import Layer


class Moves(Layer):
    """Shows the pokemon's list of moves."""

    SELECTED_SPRITE = "SELECTED_SPRITE"
    PP = "PP"

    is_event_handler = True

    def __init__(self, pokemon, selected=0):
        super().__init__()
        self._pokemon = pokemon
        self._selected = selected

        self._is_visible = False
        self._actions = dict()
        self.update_moves()

        self._actions[len(self._actions)] = cocos.sprite.Sprite('img/battle/moves/return.png')
        self._actions[len(self._actions) - 1].position = 615 + self._actions[len(self._actions) - 1].width, 90
        self.add(self._actions[len(self._actions) - 1])

        selected_sprite = cocos.sprite.Sprite('img/battle/moves/selected_return.png')
        selected_sprite.visible = False
        self._actions[len(self._actions) - 1].add(selected_sprite, name=Moves.SELECTED_SPRITE)

    def _update_selected_action(self):
        for action in range(len(self._actions)):
            self._actions[action].get(Moves.SELECTED_SPRITE).visible = False

        self._actions[self._selected].get(Moves.SELECTED_SPRITE).visible = True

    def on_key_press(self, key, modifiers):
        event_handled = False
        if self._is_visible:
            if key == KeyEnum.B.value or (key == KeyEnum.ENTER.value and self._selected == len(self._actions) - 1):
                self.do(CallFunc(self.toggle_apparition) + Delay(0.3) + CallFunc(self.parent.show_actions))
                event_handled = True
            elif key == KeyEnum.ENTER.value:
                self.parent.move_selected(self._pokemon.moves[self._selected])
                event_handled = True
            elif key == KeyEnum.UP.value and self._selected > 0:
                self._selected = self._selected - 1
                event_handled = True
            elif key == KeyEnum.DOWN.value and self._selected < len(self._actions) - 1:
                self._selected = self._selected + 1
                event_handled = True

            self._update_selected_action()

            return event_handled

    def toggle_apparition(self):
        for action in range(len(self._actions)):
            offset = self._actions[action].width if self._is_visible else -self._actions[action].width
            self._actions[action].do(Delay(0.1 * len(self._actions) - (0.1 * action)) + MoveBy((offset, 0), 0.2))

        self._is_visible = not self._is_visible

        if self._is_visible:
            self._selected = 0
            self._update_selected_action()

    def update_moves(self):
        for index, move in enumerate(self._pokemon.moves):
            if index in self._actions:
                self.remove(self._actions[index])

            self._actions[index] = cocos.sprite.Sprite('img/battle/moves/{0}.png'.format(move.move.type.name.lower()))
            offset = 0 if self._is_visible else self._actions[index].width
            self._actions[index].position = 575 + offset, 250 - 40 * index

            selected_sprite = cocos.sprite.Sprite(
                'img/battle/moves/selected_{0}.png'.format(move.move.type.name.lower()))
            selected_sprite.visible = False
            self._actions[index].add(selected_sprite, name=Moves.SELECTED_SPRITE)

            name = cocos.text.Label(move.move.name, font_size=9, anchor_x="left", anchor_y="center",
                                    color=(0, 0, 0, 255), bold=True)
            name.position = -57, 8
            self._actions[index].add(name)

            pp = cocos.text.Label("PP {0}/{1}".format(move.current_pp, move.pp),
                                  font_size=9, anchor_x="left", anchor_y="center", bold=True)
            pp.position = (-15, -8)
            self._actions[index].add(pp, name=Moves.PP)
            type = cocos.sprite.Sprite('img/common/types/{0}.png'.format(move.move.type.name.lower()))
            type.position = (-35, -8)
            type.scale = 0.9
            self._actions[index].add(type)

            self.add(self._actions[index])
