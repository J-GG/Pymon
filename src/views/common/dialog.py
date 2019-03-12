import typing

import cocos
from cocos.actions import *

from views.common.key_enum import KeyEnum
from views.common.layer import Layer


class Dialog(Layer):
    """Show a text to the user."""

    is_event_handler = True

    def __init__(self) -> None:
        """Create a dialog layer showing text to the player."""

        super().__init__()

        self._background = cocos.sprite.Sprite('img/common/dialog_background.png', anchor=(0, 0))
        self._background.position = (0, 0)
        self.add(self._background)

        self._cursor = cocos.sprite.Sprite('img/common/cursor.png')
        self._cursor.position = (625, 15)
        self._cursor.do(Repeat(MoveBy((0, 5), 0.5) + MoveBy((0, -5), 0.5)))
        self._cursor.visible = False
        self.add(self._cursor)

        self._label = cocos.text.Label("")
        self.add(self._label)

        self._text = []
        self._text_index = 0
        self._start_index = 0
        self._end_index = 0
        self._callback = None
        self._split_text = []

    def set_text(self, text: typing.Union[str, typing.List[str]], callback: typing.Callable = None) -> None:
        """Set the text to be displayed.

        :param text: The text or a list of texts to be displayed.
            If it is a list, the player is required to press enter between
            each message.
        :param callback: The function called when the user finished reading
        the text.
        """

        self._text = text if isinstance(text, list) else [text]
        self._text_index = 0
        self._split_text = self._text[self._text_index].split(" ")
        self._start_index = 0
        self._end_index = 0
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

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Show the next part of the text if there is some left by pressing ENTER.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False

        if key == KeyEnum.ENTER.value and self._cursor.visible:
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
                    self._callback()

            event_handled = True

        return event_handled
