import cocos

from views.common.layer import Layer


class ActionsLayer(Layer):
    """Shows the list of actions available to the player."""

    SELECTED_SPRITE = "SELECTED_SPRITE"

    is_event_handler = True

    def __init__(self) -> None:
        """Create a layer with the list of actions and manage their interaction."""

        super().__init__()

    def on_key_press(self, key, modifiers) -> bool:
        """Manage the key press event.

        Update the selected action when pressing UP or BOTTOM.
        Activate the selected action when pressing ENTER.

        :param key: The pressed key.
        :param modifiers: The pressed modifiers.
        :return Whether the event has been handled.
        """

        event_handled = False

        cocos.director.director.pop()

        return event_handled
