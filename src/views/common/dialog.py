import typing

import cocos
import pyglet
from cocos.actions import *
from pyglet.window import key as keys

from toolbox.init import PATH
from views.common.layer import Layer


class Dialog(Layer):
    """Show a text to the user."""

    is_event_handler = True

    def __init__(self) -> None:
        """Create a dialog layer showing text to the player."""

        super().__init__()

        self._background = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/common/dialog_background.png'), anchor=(0, 0))
        self._background.position = (0, 0)
        self.add(self._background)

        self._cursor = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/common/cursor.png'))
        self._cursor.position = (625, 15)
        self._cursor.do(Repeat(MoveBy((0, 5), 0.5) + MoveBy((0, -5), 0.5)))
        self._cursor.visible = False
        self.add(self._cursor)

        self._label = cocos.text.Label("")
        self.add(self._label)

        self._choices_background = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/common/dialog_choices_background.png'), anchor=(0, 0))
        self._choices_background.position = (
            cocos.director.director.get_window_size()[0] - self._choices_background.width - 20, 80)
        self._choices_background.visible = False
        self.add(self._choices_background)

        self._choices_cursor = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/common/cursor_white.png'), anchor=(0, 0))
        self._choices_cursor.do(RotateBy(-90, 0))
        self._choices_cursor.visible = False
        self.add(self._choices_cursor)

        self._choices_labels = []

        self._text = []
        self._text_index = 0
        self._start_index = 0
        self._end_index = 0
        self._choices = None
        self._selected_choice = None
        self._callback = None
        self._split_text = []

    def set_text(self, text: typing.Union[str, typing.List[str]], callback: typing.Callable = None,
                 choices: typing.List[str] = None) -> None:
        """Set the text to be displayed.

        :param text: The text or a list of texts to be displayed.
            If it is a list, the player is required to press enter between
            each message.
        :param callback: The function called when the user finished reading.
        :param choices: The list of choices the player can choose among.
        the text.
        """

        self._text = text if isinstance(text, list) else [text]
        self._text_index = 0
        self._split_text = self._text[self._text_index].split(" ")
        self._start_index = 0
        self._end_index = 0
        self._selected_choice = None
        self._choices = choices
        self._callback = callback
        self._update_text()

    def _update_text(self) -> None:
        """Display the text. Cut it if necessary.
        
        If the text is cut, the cursor gets visible and the user needs to press
        Enter to show the rest of the text.
        """

        self.remove(self._label)
        self._cursor.visible = False if not self._callback else True

        self._label = self._get_label(self._start_index)

        if self._choices and self._end_index == len(self._split_text):
            self._show_choices()
            self._selected_choice = 0
            self._update_choices_cursor()

        self._label.position = (10, 30)
        self.add(self._label)

    def _get_label(self, end_index: int) -> cocos.text.Label:
        """Get the label to the displayed to the user.

        It optimizes the screen space by showing as much text as possible and
        cutting if it is too long.

        :param end_index: The index until which the text should be included.
        :return: The label to be displayed to the user.
        """

        label = cocos.text.Label(" ".join(self._split_text[self._start_index:end_index]),
                                 width=cocos.director.director.get_window_size()[0] - 10,
                                 multiline=True)
        if label.element.content_height <= 36 and len(self._split_text) > end_index:
            return self._get_label(end_index + 1)
        else:
            self._end_index = end_index - 2 if len(self._split_text) > end_index else end_index
            if self._end_index != len(self._split_text) or len(self._text) > self._text_index + 1:
                self._cursor.visible = True

            return cocos.text.Label(" ".join(self._split_text[self._start_index:self._end_index]),
                                    width=cocos.director.director.get_window_size()[0] - 10,
                                    multiline=True)

    def _show_choices(self) -> None:
        """Show the list of choices to the player."""

        self._choices_background.visible = True
        self._cursor.visible = False

        for index, choice_text in enumerate(self._choices):
            choice_label = cocos.text.Label(choice_text)
            choice_label.position = (cocos.director.director.get_window_size()[0] - 60, 130 - index * 30)
            self._choices_labels.append(choice_label)
            self.add(choice_label)

    def _update_choices_cursor(self) -> None:
        """Update the position of the cursor."""

        self._choices_cursor.visible = True
        self._choices_cursor.position = (
            cocos.director.director.get_window_size()[0] - self._choices_background.width + 5,
            130 - self._selected_choice * 30 - 3)

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Show the next part of the text if there is some left by pressing ENTER.
        Call the callback function if there is some and send the potential
        answer to the question.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False

        if key == keys.ENTER and self._cursor.visible:
            if self._end_index != len(self._split_text):
                self._start_index = self._end_index
                self._update_text()
            elif self._end_index == len(self._split_text) and len(self._text) > self._text_index + 1:
                self._text_index += 1
                self._start_index = 0
                self._end_index = 0
                self._split_text = self._text[self._text_index].split(" ")
                self._update_text()
            else:
                self._cursor.visible = False
                if self._callback:
                    if self._selected_choice is None:
                        self._callback()
        elif key == keys.ENTER and not self._cursor.visible and self._choices:
            self._choices_cursor.visible = False
            self._choices_background.visible = False
            for choice in self._choices_labels:
                self.remove(choice)
            self._choices_labels = []

            self._callback(self._selected_choice)
            event_handled = True
        elif key == keys.UP and self._selected_choice is not None:
            self._selected_choice = 0 if self._selected_choice <= 1 else self._selected_choice - 1
            self._update_choices_cursor()
            event_handled = True
        elif key == keys.DOWN and self._selected_choice is not None:
            self._selected_choice = len(self._choices) - 1 if self._selected_choice >= len(
                self._choices) - 2 else self._selected_choice + 1
            self._update_choices_cursor()
            event_handled = True

        return event_handled
