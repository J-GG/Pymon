import cocos


class Background(cocos.layer.Layer):
    """The background of a fight.

    Attributes:
        - FIGHT_BACKGROUND: contains all of the background which can be used.
    """

    FIGHT_BACKGROUND = ["bridge.png", "cave.jpg", "city.png", "clearing.png", "forest.png", "meadow.jpg"]

    def __init__(self):
        super(Background, self).__init__()

        self._background = cocos.sprite.Sprite('fight/backgrounds/{0}'.format((Background.FIGHT_BACKGROUND[3])))
        self.add(self._background)
