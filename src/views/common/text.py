import cocos
import pyglet

from toolbox.init import PATH


class Text(cocos.cocosnode.CocosNode):
    """Enables to write text with the Pokemon font.

    Attributes:
        - characters: List of characters for which a special process is 
            necessary.
    """

    characters = dict()
    characters["/"] = ("slash", False)
    characters[" "] = ("blank_space", False)
    characters["j"] = ("j", True)
    characters["p"] = ("p", True)
    characters["q"] = ("q", True)

    def __init__(self, text: str) -> None:
        """Create a new text to be displayed.

        :param text: The text to be displayed.
        """

        super().__init__()

        self._width = 0
        self._opacity = 255
        self._sprites = []
        self._text = text
        for index, c in enumerate(text):
            y_offset = 0
            if c in Text.characters:
                if Text.characters[c][1]:
                    y_offset = 2
                c = Text.characters[c][0]
            elif c.isupper():
                c = c.lower() + "_maj"
            self._sprites.append(
                cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/common/font/{0}.png'.format(c))))
            self._sprites[index].position = self._width, (self._sprites[index].height - 11) / 2 - y_offset
            self._width += self._sprites[index].width
            self.add(self._sprites[index])

    @property
    def text(self) -> str:
        """Get the text.

        :return: The text.
        """

        return self._text

    @property
    def width(self) -> int:
        """Get the with of the text.

        :return: The width of the text.
        """

        return self._width

    @property
    def opacity(self) -> int:
        """Get the opacity of the text.

        :return: The opacity of the text.
        """

        return self._opacity

    @opacity.setter
    def opacity(self, opacity: int) -> None:
        """Set the opacity of the text.

        :param opacity: The opacity of the text.
        """

        for sprite in self._sprites:
            sprite.opacity = opacity
