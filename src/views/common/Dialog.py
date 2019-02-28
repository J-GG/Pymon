import cocos

from toolbox.layer import Layer


class Dialog(Layer):
    """Show a text to a user."""

    def __init__(self):
        super(Dialog, self).__init__()

        self._background = cocos.sprite.Sprite('common/dialog_background.png', anchor=(0, 0))
        self._background.position = (0, 0)
        self.add(self._background)

        self._text = cocos.text.Label("")
        self.add(self._text)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self.remove(self._text)
        self._text = cocos.text.Label(text)
        self._text.position = (10, 30)
        self.add(self._text)
