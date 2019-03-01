from views.battle.battle import BattleScene


class BattleController:
    """Manages the battle."""

    @staticmethod
    def battle():
        BattleScene()

    @staticmethod
    def run():
        from controllers.main_menu import MainMenuController
        MainMenuController().show_menu()
