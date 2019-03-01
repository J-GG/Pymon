import cocos


class Background(cocos.layer.Layer):
    """The background of a battle.

    Attributes:
        - BATTLE_BACKGROUND: contains all of the background which can be used.
    """

    BATTLE_BACKGROUND = ["bridge.png", "cave.jpg", "city.png", "clearing.png", "forest.png", "meadow.jpg"]

    def __init__(self):
        super(Background, self).__init__()

        self._background = cocos.sprite.Sprite('battle/backgrounds/{0}'.format((Background.BATTLE_BACKGROUND[3])))
        self.add(self._background)
