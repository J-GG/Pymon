from views.intro.intro_scene import IntroScene


class IntroController:
    """Manages the introduction of the game."""

    @staticmethod
    def show_intro() -> None:
        """Show the intro of the game."""

        IntroScene()
