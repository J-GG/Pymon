import cocos
import pyglet
from pyglet.window import key as keys

from toolbox.game import Game
from toolbox.i18n import I18n
from toolbox.init import PATH


class ActionsLayer(cocos.layer.Layer):
    """Display and manage the item which can be selected by the user:
    - Continue
    - New Game
    - Settings
    """

    CONTINUE = 0
    NEW_GAME = 1
    SETTINGS = 2
    ACTIONS = [CONTINUE, NEW_GAME, SETTINGS]

    SELECTED_SPRITE = "SELECTED_SPRITE"

    is_event_handler = True

    def __init__(self) -> None:
        """Create the list of actions available in the main menu."""

        super().__init__()

        self._game_state = None if Game().game_state.time == 0 else Game().game_state
        self._actions = []

        continue_file = "multi_line_action" if self._game_state else "multi_line_action_disabled"
        continue_sprite = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/main_menu/{0}.jpg'.format(continue_file)))
        continue_sprite.position = (320, 355)
        continue_selected = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/main_menu/multi_line_action_selected.jpg'))
        continue_sprite.add(continue_selected, name=ActionsLayer.SELECTED_SPRITE)
        continue_text = cocos.text.Label(I18n().get("MAIN_MENU.CONTINUE"), bold=True, color=(0, 0, 0, 255))
        continue_text.position = (-180, 60)
        continue_sprite.add(continue_text)
        if self._game_state:
            player = cocos.text.Label(I18n().get("MAIN_MENU.PLAYER"), bold=True, color=(16, 173, 231, 255))
            player.position = (-130, 30)
            continue_sprite.add(player)
            player_name = cocos.text.Label(self._game_state.player.name, bold=True, color=(16, 173, 231, 255),
                                           anchor_x="right")
            player_name.position = (70, 30)
            continue_sprite.add(player_name)
            time = cocos.text.Label(I18n().get("MAIN_MENU.TIME"), bold=True, color=(16, 173, 231, 255))
            time.position = (-130, 0)
            continue_sprite.add(time)
            hours = int(self._game_state.time // 3600)
            minutes = int((self._game_state.time - (hours * 3600)) // 60)
            time_value = cocos.text.Label("{:02d}:{:02d}".format(hours, minutes), bold=True, color=(16, 173, 231, 255),
                                          anchor_x="right")
            time_value.position = (70, 0)
            continue_sprite.add(time_value)
            for index, pokemon in enumerate(self._game_state.player.pokemons):
                pokemon_sprite = cocos.sprite.Sprite(
                    pyglet.image.load(PATH + '/assets/img/pokemon/mini/{0}.png'.format(pokemon.species.id.lower())))
                pokemon_sprite.scale = 0.7
                pokemon_sprite.position = (-140 + index * 60, -50)
                continue_sprite.add(pokemon_sprite)
        self.add(continue_sprite)
        self._actions.append(continue_sprite)

        new_game = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action.jpg'))
        new_game.position = (320, 196)
        new_game_selected = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action_selected.jpg'))
        new_game.add(new_game_selected, name=ActionsLayer.SELECTED_SPRITE)
        new_game_text = cocos.text.Label(I18n().get("MAIN_MENU.NEW_GAME"), bold=True, color=(0, 0, 0, 255))
        new_game_text.position = (-180, -5)
        new_game.add(new_game_text)
        self.add(new_game)
        self._actions.append(new_game)

        settings = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action.jpg'))
        settings.position = (320, 91)
        settings_selected = cocos.sprite.Sprite(
            pyglet.image.load(PATH + '/assets/img/main_menu/single_line_action_selected.jpg'))
        settings.add(settings_selected, name=ActionsLayer.SELECTED_SPRITE)
        settings_text = cocos.text.Label(I18n().get("MAIN_MENU.SETTINGS"), bold=True, color=(0, 0, 0, 255))
        settings_text.position = (-180, -5)
        settings.add(settings_text)
        self.add(settings)
        self._actions.append(settings)

        self._choice = 0 if self._game_state else 1
        self._update_screen()

    def _update_screen(self) -> None:
        """update the selected action."""

        for i in range(len(ActionsLayer.ACTIONS)):
            if self._choice == i:
                self._actions[i].get(ActionsLayer.SELECTED_SPRITE).visible = True
            else:
                self._actions[i].get(ActionsLayer.SELECTED_SPRITE).visible = False

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected action when pressing UP or BOTTOM.
        Activate the selected action when pressing ENTER.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False

        if key == keys.UP and self._choice > 0 and (self._game_state or self._choice > 1):
            self._choice -= 1
            event_handled = True
        elif key == keys.DOWN and self._choice < len(ActionsLayer.ACTIONS) - 1:
            self._choice += 1
            event_handled = True
        elif key == keys.ENTER:
            if self._choice == ActionsLayer.CONTINUE:
                self.parent.continue_game()
            elif self._choice == ActionsLayer.NEW_GAME:
                self.parent.new_game()
            else:
                self.parent.settings()
            event_handled = True

        self._update_screen()

        return event_handled
