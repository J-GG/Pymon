class MainMenuController:
    """Manages the main menu."""

    @staticmethod
    def show_menu() -> None:
        """Show the main menu of the game."""

        from views.main_menu.main_menu_scene import MainMenuScene
        MainMenuScene()
