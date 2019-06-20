import cocos
import pyglet
from cocos.actions import *
from pyglet.window import key as keys

from models.settings.controls_enum import ControlsEnum
from models.settings.language_enum import LanguageEnum
from models.settings.settings_model import SettingsModel
from toolbox.game import Game
from toolbox.i18n import I18n
from toolbox.init import PATH
from toolbox.keyboard import is_key_up, is_key_down, is_key_right, is_key_left, is_key_action, is_key_cancel


class ActionsLayer(cocos.layer.Layer):
    """Display and manage the settings the player can set."""

    LANGUAGE = "LANGUAGE"
    CANCEL = "CANCEL_BTN"

    SELECTED_SPRITE = "SELECTED_SPRITE"
    LANGUAGE_VALUE = "LANGUAGE_VALUE"
    CONTROL_VALUE = "CONTROL_VALUE"

    is_event_handler = True

    def __init__(self, settings: SettingsModel) -> None:
        """Create the list of settings.

        :param settings: The player's settings.
        """

        super().__init__()

        self._actions = dict()

        self._selected_language = settings.language.index
        language = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action.jpg'))
        language.position = (320, 445)
        language_selected = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action_selected.jpg'))
        language.add(language_selected, name=ActionsLayer.SELECTED_SPRITE)
        language_text = cocos.text.Label(I18n().get("SETTINGS.LANGUAGE"), bold=True, color=(0, 0, 0, 255))
        language_text.position = (-180, -5)
        language.add(language_text)
        language_value = cocos.text.Label(I18n().get("SETTINGS.LANGUAGE.{0}".format(settings.language.name)), bold=True,
                                          color=(0, 0, 0, 255))
        language_value.position = (70, -5)
        language.add(language_value, name=ActionsLayer.LANGUAGE_VALUE)
        language_left_arrow = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/common/cursor.png'))
        language_left_arrow.do(RotateBy(90, 0))
        language_left_arrow.position = (40, 0)
        language.add(language_left_arrow)
        language_right_arrow = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/common/cursor.png'))
        language_right_arrow.do(RotateBy(-90, 0))
        language_right_arrow.position = (170, 0)
        language.add(language_right_arrow)

        self._actions[ActionsLayer.LANGUAGE] = language
        self.add(language, name=str(ActionsLayer.LANGUAGE))

        for index, control in enumerate(ControlsEnum):
            control_sprite = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action.jpg'))
            control_sprite.position = (320, 445 - (control_sprite.height + 9) * (index + 1))
            control_sprite_selected = cocos.sprite.Sprite(
                pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action_selected.jpg'))
            control_sprite.add(control_sprite_selected, name=ActionsLayer.SELECTED_SPRITE)
            control_text = cocos.text.Label(I18n().get("CONTROLS.{0}".format(control.name)), bold=True,
                                            color=(0, 0, 0, 255))
            control_text.position = (-180, -5)
            control_sprite.add(control_text)
            control_value = cocos.text.Label(str(keys.symbol_string(Game().settings.controls[control])), bold=True,
                                             color=(0, 0, 0, 255))
            control_value.position = (70, -5)
            control_sprite.add(control_value, name=ActionsLayer.CONTROL_VALUE)

            self._actions[control.name] = control_sprite
            self.add(control_sprite, name=str(control))

        cancel = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/main_menu/single_little_line_action.jpg'))
        cancel.position = (320, 34)
        cancel_selected = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/main_menu/single_little_line_action_selected.jpg'))
        cancel.add(cancel_selected, name=ActionsLayer.SELECTED_SPRITE)
        cancel_text = cocos.text.Label(I18n().get("SETTINGS.CANCEL"), bold=True, color=(0, 0, 0, 255))
        cancel_text.position = (-cancel_text.element.content_width / 2, -5)
        cancel.add(cancel_text)
        self._actions[ActionsLayer.CANCEL] = cancel
        self.add(cancel)

        self._choice = 0
        self._update_screen()

    def _update_screen(self) -> None:
        """Update the selected action."""

        for index, action in enumerate(self._actions):
            if self._choice == index:
                self._actions[action].get(ActionsLayer.SELECTED_SPRITE).visible = True
            else:
                self._actions[action].get(ActionsLayer.SELECTED_SPRITE).visible = False

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected action when pressing UP or BOTTOM.
        Change the value of the settings with RIGHT or LEFT.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False

        if is_key_up(key) and self._choice > 0:
            self._choice -= 1
            event_handled = True
        elif is_key_down(key) and self._choice < len(self._actions) - 1:
            self._choice += 1
            event_handled = True
        elif self._actions[ActionsLayer.LANGUAGE].get(ActionsLayer.SELECTED_SPRITE).visible and (
                is_key_left(key) or is_key_right(key)):
            if is_key_left(key):
                self._selected_language = self._selected_language - 1 if self._selected_language > 0 else len(
                    LanguageEnum) - 1
            elif is_key_right(key):
                self._selected_language = self._selected_language + 1 if self._selected_language < len(
                    LanguageEnum) - 1 else 0
            self.get(str(ActionsLayer.LANGUAGE)).get(ActionsLayer.LANGUAGE_VALUE).element.text = I18n().get(
                "SETTINGS.LANGUAGE.{0}".format(LanguageEnum.from_index(self._selected_language).name))
            event_handled = True
        elif (is_key_action(key) and self._actions[ActionsLayer.CANCEL].get(
                ActionsLayer.SELECTED_SPRITE).visible) or is_key_cancel(key):
            new_settings = {LanguageEnum: LanguageEnum.from_index(self._selected_language)}
            self.parent.cancel_settings(new_settings)
            event_handled = True

        self._update_screen()

        return event_handled
