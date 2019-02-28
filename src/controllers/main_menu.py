import cocos

from toolbox.singleton import Singleton
from views.main_menu.main_menu import MainMenuScene


class MainMenuController(metaclass=Singleton):
    """Manages the main menu."""

    def show_menu(self):
        cocos.director.director.run(MainMenuScene())
