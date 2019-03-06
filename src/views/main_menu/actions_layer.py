import cocos

from controllers.battle_controller import BattleController
from views.common.key_enum import KeyEnum


class ActionsLayer(cocos.layer.Layer):
    """The item which can be selected by the user:
    - Continue
    - New Game
    """
    is_event_handler = True

    def __init__(self) -> None:
        """Create the list of actions available in the main menu."""

        super().__init__()

        self._new_game_off = cocos.sprite.Sprite('img/main_menu/new_game_off.gif')
        self._new_game_off.position = (320, 120)
        self.add(self._new_game_off)

        self._new_game_on = cocos.sprite.Sprite('img/main_menu/new_game_on.gif')
        self._new_game_on.position = (320, 120)
        self.add(self._new_game_on)

        self._load_game_off = cocos.sprite.Sprite('img/main_menu/load_game_off.gif')
        self._load_game_off.position = (320, 320)
        self.add(self._load_game_off)

        self._load_game_on = cocos.sprite.Sprite('img/main_menu/load_game_on.gif')
        self._load_game_on.position = (320, 320)
        self.add(self._load_game_on)

        self._choice = 0
        self._update_screen()

    def _update_screen(self) -> None:
        """update the actions visible."""

        self._load_game_off.visible = self._choice != 0
        self._load_game_on.visible = self._choice == 0
        self._new_game_off.visible = self._choice != 1
        self._new_game_on.visible = self._choice == 1

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected action when pressing UP or BOTTOM.
        Activate the selected action when pressing ENTER.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False

        if key == KeyEnum.UP.value:
            self._choice = 0
            event_handled = True
        elif key == KeyEnum.DOWN.value:
            self._choice = 1
            event_handled = True
        elif key == KeyEnum.ENTER.value:
            BattleController().battle()
            event_handled = True

        self._update_screen()

        return event_handled
