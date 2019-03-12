import cocos


class BackgroundLayer(cocos.layer.ColorLayer):
    """The background of the settings."""

    def __init__(self) -> None:
        """Create a new background for the settings."""

        super().__init__(255, 255, 255, 255)
