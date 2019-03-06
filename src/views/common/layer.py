import cocos


class Layer(cocos.layer.Layer):
    """Enables to update the opacity of a layer's children when its opacity is
     modified."""

    def __init__(self) -> None:
        """Create a new layer."""

        super().__init__()
        self._opacity = 255

    @property
    def opacity(self) -> int:
        """Get the opacity of the layer.

        :return: the opacity of the layer.
        """

        return self._opacity

    @opacity.setter
    def opacity(self, opacity: int) -> None:
        """Set the opacity of the layer and update its children' opacity.

        :param opacity: The opacity of the layer.
        """

        self._opacity = opacity
        for child in self.children:
            if hasattr(child[1], "opacity"):
                child[1].opacity = opacity
