import cocos


class Background(cocos.layer.ColorLayer):
    """The background of the introduction."""

    def __init__(self) -> None:
        """Create a new background for the intro."""

        super().__init__(0, 0, 0, 255)
