import cocos


class BackgroundLayer(cocos.layer.ColorLayer):
    """The background of the main menu."""

    def __init__(self) -> None:
        """Create a new background for the main menu."""

        super().__init__(255, 255, 255, 255)
