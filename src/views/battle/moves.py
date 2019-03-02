import cocos
from cocos.actions import *

from views.common.key_enum import KeyEnum
from views.common.layer import Layer


class Moves(Layer):
    """Shows the pokemon's list of moves."""

    is_event_handler = True

    def __init__(self, pokemon, selected=0):
        super().__init__()
        self._selected = selected

        self._isVisible = False
        self._actions = dict()
        self._selections = dict()
        for index, move in enumerate(pokemon.moves):
            self._actions[index] = cocos.sprite.Sprite('img/battle/moves/{0}.png'.format(move.move.type.name.lower()))
            self._actions[index].position = 567 + self._actions[index].width, 250 - 40 * index
            name = cocos.text.Label(move.move.name, font_size=9, anchor_x="left", anchor_y="center",
                                    color=(0, 0, 0, 255), bold=True)
            name.position = (-57, 8)
            self._actions[index].add(name)
            pp = cocos.text.Label("PP {0}/{1}".format(move.current_pp, move.pp),
                                  font_size=9, anchor_x="left", anchor_y="center", bold=True)
            pp.position = (-15, -8)
            self._actions[index].add(pp)
            type = cocos.sprite.Sprite('img/common/types/{0}.png'.format(move.move.type.name.lower()))
            type.position = (-35, -8)
            type.scale = 0.9
            self._actions[index].add(type)
            self.add(self._actions[index])

            self._selections[index] = cocos.sprite.Sprite(
                'img/battle/moves/selected_{0}.png'.format(move.move.type.name.lower()))
            self._selections[index].position = 567 + self._actions[index].width, 250 - 40 * index
            name = cocos.text.Label(move.move.name, font_size=9, anchor_x="left", anchor_y="center",
                                    color=(0, 0, 0, 255), bold=True)
            name.position = (-57, 8)
            self._selections[index].add(name)
            pp = cocos.text.Label("PP {0}/{1}".format(move.current_pp, move.pp),
                                  font_size=9, anchor_x="left", anchor_y="center", bold=True)
            pp.position = (-15, -8)
            self._selections[index].add(pp)
            type = cocos.sprite.Sprite('img/common/types/{0}.png'.format(move.move.type.name.lower()))
            type.position = (-35, -8)
            type.scale = 0.9
            self._selections[index].add(type)
            self._selections[index].visible = False
            self.add(self._selections[index])

        self._actions[len(self._actions)] = cocos.sprite.Sprite('img/battle/moves/return.png')
        self._actions[len(self._actions) - 1].position = 615 + self._actions[len(self._actions) - 1].width, 90
        self.add(self._actions[len(self._actions) - 1])

        self._selections[len(self._selections)] = cocos.sprite.Sprite('img/battle/moves/selected_return.png')
        self._selections[len(self._selections) - 1].position = self._actions[len(self._actions) - 1].position
        self._selections[len(self._selections) - 1].visible = False
        self.add(self._selections[len(self._selections) - 1])

        self._actions[self._selected].visible = False
        self._selections[self._selected].visible = True

    def _update_selection(self):
        for action in range(len(self._actions)):
            self._actions[action].visible = True
            self._selections[action].visible = False

        self._actions[self._selected].visible = False
        self._selections[self._selected].visible = True

    def on_key_press(self, key, modifiers):
        event_handled = False
        if self._isVisible:
            if key == KeyEnum.B.value or (key == KeyEnum.ENTER.value and self._selected == len(self._selections) - 1):
                self.do(CallFunc(self.toggle_apparition) + Delay(0.3) + CallFunc(self.parent.show_actions))
                event_handled = True
            elif key == KeyEnum.UP.value and self._selected > 0:
                self._selected = self._selected - 1
                event_handled = True
            elif key == KeyEnum.DOWN.value and self._selected < 4:
                self._selected = self._selected + 1
                event_handled = True

            self._update_selection()

            return event_handled

    def toggle_apparition(self):
        for action in range(len(self._actions)):
            offset = self._selections[action].width if self._isVisible else -self._selections[action].width
            self._actions[action].do(Delay(0.1 * len(self._actions) - (0.1 * action)) + MoveBy((offset, 0), 0.2))
            self._selections[action].do(Delay(0.1 * len(self._actions) - (0.1 * action)) + MoveBy((offset, 0), 0.2))

        self._isVisible = not self._isVisible

        if self._isVisible:
            self._selected = 0
            self._update_selection()
