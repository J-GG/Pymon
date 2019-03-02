import cocos

from models.stat_enum import StatEnum
from views.common.layer import Layer
from views.common.text import Text


class OpponentHUD(Layer):
    """The information about the opponent pokemon: name, level, HP"""

    def __init__(self, pokemon):
        super().__init__()

        self._name = Text(pokemon.nickname)
        self._name.position = 400 - self._name.width, 370
        self.add(self._name, z=1)

        self._level_txt = cocos.sprite.Sprite('img/battle/hud/level.png')
        self._level_txt.position = 405, 368
        self.add(self._level_txt, z=1)

        self._level = Text(str(pokemon.level))
        self._level.position = 417, 370
        self.add(self._level, z=1)

        self._hp_bar = cocos.sprite.Sprite('img/battle/hud/hp_bar.png')
        self._hp_bar.position = 395, 358
        self.add(self._hp_bar)

        self._hp_bar_content = []
        hp_bar_size = 48 * pokemon.current_stats[StatEnum.HP.name] // pokemon.stats[StatEnum.HP.name]
        if hp_bar_size * 100 // 48 > 50:
            bar_color = "green"
        elif hp_bar_size * 100 // 48 < 20:
            bar_color = "red"
        else:
            bar_color = "yellow"
        for i in range(48):
            self._hp_bar_content.append(cocos.sprite.Sprite('img/battle/hud/hp_bar_{0}.png'.format(bar_color)))
            self._hp_bar_content[i].position = 378 + i, 358
            self.add(self._hp_bar_content[i], z=1)
