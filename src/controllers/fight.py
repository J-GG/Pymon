from toolbox.singleton import Singleton
from views.fight.fight import FightScene


class FightController(metaclass=Singleton):
    """Manages the fights."""

    def show_fight(self):
        FightScene()
