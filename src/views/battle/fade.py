import cocos

from views.common.layer import Layer


class Fade(Layer):
    """A simple fade."""

    def __init__(self):
        super(Fade, self).__init__()

        self._background = cocos.sprite.Sprite('battle/fade.jpg', anchor=(0, 0))
        self._background.position = (0, 0)
        self._background.opacity = 0
        self.add(self._background)
