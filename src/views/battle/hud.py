import cocos

from models.stat_enum import StatEnum
from views.common.layer import Layer
from views.common.text import Text


class HUD(Layer):
    """The information about the player's pokemon: name, level, HP, XP"""

    def __init__(self, pokemon):
        super().__init__()
        self._name = Text(pokemon.nickname)
        self._name.position = 450 - self._name.width, 230
        self.add(self._name, z=1)

        self._level_txt = cocos.sprite.Sprite('img/battle/hud/level.png')
        self._level_txt.position = 455, 228
        self.add(self._level_txt, z=1)

        self._level = Text(str(pokemon.level))
        self._level.position = 467, 230
        self.add(self._level, z=1)

        self._hp_bar = cocos.sprite.Sprite('img/battle/hud/hp_bar.png')
        self._hp_bar.position = 444, 218
        self.add(self._hp_bar)

        self._hp_bar_content = []
        hp_bar_size = 48 * pokemon.current_stats[StatEnum.HP.name] // pokemon.stats[StatEnum.HP.name]
        if hp_bar_size * 100 // 48 > 50:
            bar_color = "green"
        elif hp_bar_size * 100 // 48 < 20:
            bar_color = "red"
        else:
            bar_color = "yellow"
        for i in range(hp_bar_size):
            self._hp_bar_content.append(cocos.sprite.Sprite('img/battle/hud/hp_bar_{0}.png'.format(bar_color)))
            self._hp_bar_content[i].position = 427 + i, 218
            self.add(self._hp_bar_content[i], z=1)

        self._hp = Text("{0}/{1}".format(pokemon.current_stats[StatEnum.HP.name], pokemon.stats[StatEnum.HP.name]))
        self._hp.position = 427, 206
        self.add(self._hp, z=1)

        self._xp_bar = cocos.sprite.Sprite('img/battle/hud/xp_bar.png')
        self._xp_bar.position = 435, 195
        self.add(self._xp_bar)

        self._current_xp_bar = []
        current_xp_bar_size = 93 * (pokemon.experience - pokemon.species.experience_function.get_xp_for_level(
            pokemon.level)) // (
                                      pokemon.experience_for_next_level - pokemon.species.experience_function.get_xp_for_level(
                                  pokemon.level))
        for i in range(current_xp_bar_size):
            self._current_xp_bar.append(cocos.sprite.Sprite('img/battle/hud/xp_bar_blue.png'))
            self._current_xp_bar[i].position = 390 + i, 195
            self.add(self._current_xp_bar[i], z=1)
