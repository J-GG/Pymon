import cocos

from toolbox.key_enum import KeyEnum


class Actions(cocos.layer.Layer):
    """The item which can be selected by the user:
    - Continue
    - New Game
    """
    is_event_handler = True

    def __init__(self):
        super(Actions, self).__init__()

        self._new_game_off = cocos.sprite.Sprite('main_menu/new_game_off.gif')
        self._new_game_off.position = (320, 120)
        self.add(self._new_game_off)

        self._new_game_on = cocos.sprite.Sprite('main_menu/new_game_on.gif')
        self._new_game_on.position = (320, 120)
        self.add(self._new_game_on)

        self._load_game_off = cocos.sprite.Sprite('main_menu/load_game_off.gif')
        self._load_game_off.position = (320, 320)
        self.add(self._load_game_off)

        self._load_game_on = cocos.sprite.Sprite('main_menu/load_game_on.gif')
        self._load_game_on.position = (320, 320)
        self.add(self._load_game_on)

        self._choice = 0
        self._update_screen()

    def _update_screen(self):
        self._load_game_off.visible = self._choice != 0
        self._load_game_on.visible = self._choice == 0
        self._new_game_off.visible = self._choice != 1
        self._new_game_on.visible = self._choice == 1

    def on_key_press(self, key, modifiers):
        if key == KeyEnum.UP.value:
            self._choice = 0
        elif key == KeyEnum.DOWN.value:
            self._choice = 1
        elif key == KeyEnum.ENTER.value:
            pass

        self._update_screen()
