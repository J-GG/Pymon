import cocos
from cocos.actions import *

from views.battle.actions_enum import ActionEnum
from views.common.key_enum import KeyEnum
from views.common.layer import Layer


class Actions(Layer):
    """Shows the list of actions available to the player."""

    SELECTED_SPRITE = "SELECTED_SPRITE"

    is_event_handler = True

    def __init__(self, selected: ActionEnum = ActionEnum.FIGHT) -> None:
        """Create a layer with the list of actions and manage their interaction.

        :param selected: The selected action.
        """

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

    def _update_selection(self) -> None:
        """Show the selected sprite of the selected action."""

        for action in ActionEnum:
            self._actions[action.name].get(Actions.SELECTED_SPRITE).visible = False

        self._actions[self._selected.name].get(Actions.SELECTED_SPRITE).visible = True

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected action when pressing UP or BOTTOM.
        Activate the selected action when pressing ENTER.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

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
                    self.toggle_apparition()
                    self.parent.fight_action()
                    event_handled = True
                elif self._selected == ActionEnum.RUN:
                    self.toggle_apparition()
                    self.parent.attempt_run()
                    event_handled = True
                    
            self._update_selection()

        return event_handled

    def toggle_apparition(self) -> None:
        """Show or hide the list of actions."""

        for index, action in enumerate(ActionEnum):
            offset = self._actions[action.name].width if self._is_visible else -self._actions[action.name].width
            self._actions[action.name].do(Delay(0.1 * action.value) + MoveBy((offset, 0), 0.2))

        self._is_visible = not self._is_visible
        self._update_selection()
