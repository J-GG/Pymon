import cocos
import pyglet
from cocos.actions import *

from toolbox.init import PATH


class GoPokemonLayer(cocos.layer.Layer):
    """The animation when the player sends a pokemon"""

    TRAINER_CHARSET = pyglet.image.load(PATH + "/assets/img/battle/trainer.png")
    TRAINER_GRID = pyglet.image.ImageGrid(TRAINER_CHARSET, 1, 9, 300, 240)

    def __init__(self) -> None:
        """Create a new layer showing the animation of the player sending a
        pokemon.
        """

        super().__init__()

        self._trainer = cocos.sprite.Sprite(pyglet.image.Animation.from_image_sequence(
            GoPokemonLayer.TRAINER_GRID[:1],
            0.5,
            loop=False)
        )
        self._trainer.scale = 1.75
        self._trainer.position = -self._trainer.width / 2, -self._trainer.height / 2
        self.add(self._trainer)

        self._light = cocos.sprite.Sprite(pyglet.image.load(PATH + "/assets/img/battle/light.png"))
        self._light.position = self._light.width / 2, self._light.height / 2
        self._light.opacity = 0
        self.add(self._light)

    def flash(self, slow: bool = False) -> None:
        """Animate the light.

        :param slow: Whether the animation is slow.
        """

        delay = 0.5 if not slow else 1
        self._light.do(Delay(0.9) + FadeIn(0.4) + Delay(delay) + FadeOut(0.3))

    def animation(self):
        """Animate the trainer and the flash."""

        self._trainer.do(MoveTo((60, 90), 0.35) + CallFunc(self._trainer_animation))

    def _trainer_animation(self):
        """Animate the trainer and the flash."""

        self._trainer.kill()
        self._trainer = cocos.sprite.Sprite(pyglet.image.Animation.from_image_sequence(
            GoPokemonLayer.TRAINER_GRID,
            0.08,
            loop=False)
        )
        self._trainer.scale = 1.75
        self._trainer.position = self._trainer.width / 3.2, self._trainer.height / 3.2
        self.add(self._trainer)

        self._trainer.do(
            Delay(0.6) + MoveTo((-self._trainer.width, 0), 1))

        self.flash()
