import cocos


class Background(cocos.layer.ColorLayer):
    """The background of the main menu."""

    def __init__(self):
        super().__init__(255, 255, 255, 255)
