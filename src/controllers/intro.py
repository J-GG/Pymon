from toolbox.singleton import Singleton
from views.intro.intro import IntroScene


class IntroController(metaclass=Singleton):
    """Manages the introduction of the game."""

    def show_itro(self):
        IntroScene()
