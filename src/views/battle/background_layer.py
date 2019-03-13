import random

import cocos
import pyglet

from toolbox.init import PATH


class BackgroundLayer(cocos.layer.Layer):
    """The background of a battle.

    Attributes:
        - BATTLE_BACKGROUND: contains all of the background which can be used.
    """

    BATTLE_BACKGROUND = ["bridge.png", "cave.jpg", "city.png", "clearing.png", "forest.png", "meadow.jpg"]

    def __init__(self) -> None:
        """Create the background of the battle."""

        super().__init__()

        self._background = cocos.sprite.Sprite(pyglet.image.load(
            PATH + '/assets/img/battle/backgrounds/{0}'.format((random.choice(BackgroundLayer.BATTLE_BACKGROUND)))))
        self.add(self._background)
