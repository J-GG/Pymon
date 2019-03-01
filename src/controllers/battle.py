from toolbox.singleton import Singleton
from views.battle.battle import BattleScene


class BattleController(metaclass=Singleton):
    """Manages the battle."""

    def battle(self):
        BattleScene()

    def run(self):
        from controllers.main_menu import MainMenuController
        MainMenuController().show_menu()
