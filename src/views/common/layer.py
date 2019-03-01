import cocos


class Layer(cocos.layer.Layer):
    """Enables to update the opacity of a layer's children when its opacity is
     modified."""

    def __init__(self):
        super().__init__()
        self._opacity = 255

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        self._opacity = opacity
        for child in self.children:
            if hasattr(child[1], "opacity"):
                child[1].opacity = opacity
