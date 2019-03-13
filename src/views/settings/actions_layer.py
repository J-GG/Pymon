import cocos
import pyglet
from cocos.actions import *

from models.settings.language_enum import LanguageEnum
from models.settings.settings_model import SettingsModel
from toolbox.i18n import I18n
from toolbox.init import PATH
from views.common.key_enum import KeyEnum


class ActionsLayer(cocos.layer.Layer):
    """Display and manage the settings the player can set."""

    LANGUAGE = 0
    CANCEL = 1
    ACTIONS = [LANGUAGE, CANCEL]

    SELECTED_SPRITE = "SELECTED_SPRITE"
    LANGUAGE_VALUE = "LANGUAGE_VALUE"

    is_event_handler = True

    def __init__(self, settings: SettingsModel) -> None:
        """Create the list of settings.

        :param settings: The player's settings.
        """

        super().__init__()

        self._actions = []

        self._selected_language = settings.language.index
        language = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action.jpg'))
        language.position = (320, 355)
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

        self._actions.append(language)
        self.add(language, name=str(ActionsLayer.LANGUAGE))

        cancel = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/main_menu/single_little_line_action.jpg'))
        cancel.position = (320, 50)
        cancel_selected = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/main_menu/single_little_line_action_selected.jpg'))
        cancel.add(cancel_selected, name=ActionsLayer.SELECTED_SPRITE)
        cancel_text = cocos.text.Label(I18n().get("SETTINGS.CANCEL"), bold=True, color=(0, 0, 0, 255))
        cancel_text.position = (-cancel_text.element.content_width / 2, -5)
        cancel.add(cancel_text)
        self._actions.append(cancel)
        self.add(cancel)

        self._choice = 0
        self._update_screen()

    def _update_screen(self) -> None:
        """Update the selected action."""

        for i in range(len(ActionsLayer.ACTIONS)):
            if self._choice == i:
                self._actions[i].get(ActionsLayer.SELECTED_SPRITE).visible = True
            else:
                self._actions[i].get(ActionsLayer.SELECTED_SPRITE).visible = False

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected action when pressing UP or BOTTOM.
        Change the value of the settings with RIGHT or LEFT.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False

        if key == KeyEnum.UP.value and self._choice > 0:
            self._choice -= 1
            event_handled = True
        elif key == KeyEnum.DOWN.value and self._choice < len(ActionsLayer.ACTIONS) - 1:
            self._choice += 1
            event_handled = True
        elif self._choice == ActionsLayer.LANGUAGE and (key == KeyEnum.LEFT.value or key == KeyEnum.RIGHT.value):
            if key == KeyEnum.LEFT.value:
                self._selected_language = self._selected_language - 1 if self._selected_language > 0 else len(
                    LanguageEnum) - 1
            elif key == KeyEnum.RIGHT.value:
                self._selected_language = self._selected_language + 1 if self._selected_language < len(
                    LanguageEnum) - 1 else 0
            self.get(str(ActionsLayer.LANGUAGE)).get(ActionsLayer.LANGUAGE_VALUE).element.text = I18n().get(
                "SETTINGS.LANGUAGE.{0}".format(LanguageEnum.from_index(self._selected_language).name))
            event_handled = True
        elif key == KeyEnum.ENTER.value:
            if self._choice == ActionsLayer.CANCEL:
                new_settings = {LanguageEnum: LanguageEnum.from_index(self._selected_language)}
                self.parent.cancel_settings(new_settings)
                event_handled = True

        self._update_screen()

        return event_handled
