import cocos


class Background(cocos.layer.ColorLayer):
    """The background of the introduction."""

    def __init__(self):
        super().__init__(0, 0, 0, 255)
