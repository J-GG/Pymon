from models.persistence import Persistence
from models.settings.language_enum import LanguageEnum
from toolbox.i18n import I18n


class SettingsModel(Persistence):
    """Defines the player's settings."""

    FILE_NAME = "settings"

    def __init__(self) -> None:
        """Create a new settings."""

        super().__init__()
        self._language = LanguageEnum.ENGLISH

    @property
    def language(self) -> LanguageEnum:
        """Get the player's language.

        :return: The ``LanguageEnum`` of the player.
        """

        return self._language

    @language.setter
    def language(self, language) -> None:
        """Set the player's language.

        :param language: A ``LanguageEnum``.
        """

        self._language = language

    def save(self) -> None:
        """Save the model into a file."""

        I18n().load_translations()
        super().save()
