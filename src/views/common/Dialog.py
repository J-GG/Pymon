import cocos
from cocos.actions import *

from views.common.key_enum import KeyEnum
from views.common.layer import Layer


class Dialog(Layer):
    """Show a text to the user."""

    is_event_handler = True

    def __init__(self):
        super().__init__()

        self._background = cocos.sprite.Sprite('img/common/dialog_background.png', anchor=(0, 0))
        self._background.position = (0, 0)
        self.add(self._background)

        self._cursor = cocos.sprite.Sprite('img/common/dialog_cursor.png')
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

    def set_text(self, text, callback=None):
        """Set the text to be displayed.

        :param text: The text to be displayed.
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

    def _update_text(self):
        """Display the text. Cut it if necessary.
        
        If the text is cut, the cursor gets visible and the user needs to press
        Enter to show the rest of the text.
        """

        self.remove(self._label)
        self._cursor.visible = False if not self._callback else True

        self._label = self._get_end_index(self._start_index)

        self._label.position = (10, 30)
        self.add(self._label)

    def _get_end_index(self, end_index):
        label = cocos.text.Label(" ".join(self._split_text[self._start_index:end_index]),
                                 width=cocos.director.director.get_window_size()[0] - 10,
                                 multiline=True)
        if label.element.content_height <= 36 and len(self._split_text) > end_index:
            return self._get_end_index(end_index + 1)
        else:
            self._end_index = end_index - 2 if len(self._split_text) > end_index else end_index
            if self._end_index != len(self._split_text) or len(self._text) > self._text_index + 1:
                self._cursor.visible = True

            return cocos.text.Label(" ".join(self._split_text[self._start_index:self._end_index]),
                                    width=cocos.director.director.get_window_size()[0] - 10,
                                    multiline=True)

    def on_key_press(self, key, modifiers):
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
