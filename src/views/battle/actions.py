import cocos
from cocos.actions import *

from views.battle.actions_enum import ActionEnum
from views.common.key_enum import KeyEnum
from views.common.layer import Layer


class Actions(Layer):
    """Shows the list of actions available to the player."""

    SELECTED_SPRITE = "SELECTED_SPRITE"

    is_event_handler = True

    def __init__(self, selected=ActionEnum.FIGHT):
        super().__init__()
        self._selected = selected

        self._is_visible = False
        self._actions = dict()
        for action in ActionEnum:
            self._actions[action.name] = cocos.sprite.Sprite('img/battle/actions/action.png')
            self._actions[action.name].position = 617 + self._actions[action.name].width, 100 + 40 * action.value
            self._actions[action.name].scale = 1.2

            selected_sprite = cocos.sprite.Sprite('img/battle/actions/selected_action.png')
            selected_sprite.scale = self._actions[action.name].scale
            selected_sprite.visible = False
            self._actions[action.name].add(selected_sprite, name=Actions.SELECTED_SPRITE)

            label = cocos.text.Label(action.name, font_size=8, anchor_x="center", anchor_y="center")
            self._actions[action.name].add(label)

            self.add(self._actions[action.name])

    def _update_selection(self):
        for action in ActionEnum:
            self._actions[action.name].get(Actions.SELECTED_SPRITE).visible = False

        self._actions[self._selected.name].get(Actions.SELECTED_SPRITE).visible = True

    def on_key_press(self, key, modifiers):
        from controllers.battle import BattleController
        event_handled = False
        if self._is_visible:
            if key == KeyEnum.UP.value and self._selected.value < 3:
                self._selected = ActionEnum(self._selected.value + 1)
                event_handled = True
            elif key == KeyEnum.DOWN.value and self._selected.value > 0:
                self._selected = ActionEnum(self._selected.value - 1)
                event_handled = True
            elif key == KeyEnum.ENTER.value:
                if self._selected == ActionEnum.FIGHT:
                    self.do(CallFunc(self.toggle_apparition) + CallFunc(self.parent.fight_action))
                    event_handled = True
                elif self._selected == ActionEnum.RUN:
                    BattleController().run()
                    event_handled = True

            self._update_selection()

            return event_handled

    def toggle_apparition(self):
        for index, action in enumerate(ActionEnum):
            offset = self._actions[action.name].width if self._is_visible else -self._actions[action.name].width
            self._actions[action.name].do(Delay(0.1 * action.value) + MoveBy((offset, 0), 0.2))

        self._is_visible = not self._is_visible
        self._update_selection()

