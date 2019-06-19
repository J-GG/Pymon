import cocos
import pyglet

from toolbox.init import PATH


class BackgroundLayer(cocos.layer.Layer):
    """The background of a battle.

    Attributes:
        - BATTLE_BACKGROUND: contains all of the background which can be used.
    """

    BATTLE_BACKGROUND = ["meadow.jpg", "bridge.png", "cave.jpg", "city.png", "clearing.png", "forest.png"]

    def __init__(self, place: str) -> None:
        """Create the background of the battle.

        :param place: The place where the battle takes place.
        """

        super().__init__()

        file = next((file for file in BackgroundLayer.BATTLE_BACKGROUND if place in file),
                    BackgroundLayer.BATTLE_BACKGROUND[0])
        self._background = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/battle/backgrounds/{0}'.format(file)))
        self.add(self._background)
