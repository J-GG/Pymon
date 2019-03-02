import cocos

from views.common.layer import Layer
from views.common.text import Text


class HUD(Layer):
    """The information about the player's pokemon: name, level, HP, XP"""

    def __init__(self):
        super().__init__()
        self._name = Text("Pikachu")
        self._name.position = 450 - self._name.width, 230
        self.add(self._name, z=1)

        self._level_txt = cocos.sprite.Sprite('img/battle/hud/level.png')
        self._level_txt.position = 455, 228
        self.add(self._level_txt, z=1)

        self._level = Text("5")
        self._level.position = 467, 230
        self.add(self._level, z=1)

        self._hp_bar = cocos.sprite.Sprite('img/battle/hud/hp_bar.png')
        self._hp_bar.position = 444, 218
        self.add(self._hp_bar)

        self._hp_bar_content = []
        for i in range(48):
            self._hp_bar_content.append(cocos.sprite.Sprite('img/battle/hud/hp_bar_green.png'))
            self._hp_bar_content[i].position = 427 + i, 218
            self.add(self._hp_bar_content[i], z=1)

        self._hp = Text("19/19")
        self._hp.position = 427, 206
        self.add(self._hp, z=1)

        self._xp_bar = cocos.sprite.Sprite('img/battle/hud/xp_bar.png')
        self._xp_bar.position = 435, 195
        self.add(self._xp_bar)

        self._xp_bar_content = []
        for i in range(20):
            self._xp_bar_content.append(cocos.sprite.Sprite('img/battle/hud/xp_bar_blue.png'))
            self._xp_bar_content[i].position = 390 + i, 195
            self.add(self._xp_bar_content[i], z=1)
