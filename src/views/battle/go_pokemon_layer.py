import cocos
import pyglet
from cocos.actions import *

from toolbox.init import PATH


class GoPokemonLayer(cocos.layer.Layer):
    """The animation when the player sends a pokemon"""

    def __init__(self) -> None:
        """Create a new layer showing the animation of the player sending a
        pokemon.
        """

        super().__init__()

        self._go = cocos.sprite.Sprite(pyglet.image.load(PATH + "/assets/img/battle/send_pokemon.png"))
        self._go.position = self._go.width / 2 - 150, self._go.height / 2 - 150
        self._go.opacity = 0
        self.add(self._go)

    def animation(self):
        self._go.do((MoveBy((150, 150), 0.2) | FadeIn(0.4)) + Delay(0.5) + FadeOut(0.3))
