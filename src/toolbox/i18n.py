import codecs
from configparser import ConfigParser

from toolbox.init import PATH
from toolbox.singleton import Singleton


class I18n(metaclass=Singleton):
    """Helps to manage internationalization."""

    def __init__(self) -> None:
        """Create a new object to manage internationalization."""

        self._config_parser = ConfigParser()
        self.load_translations()

    def load_translations(self) -> None:
        """Load the translations file based on the settings."""

        from toolbox.game import Game

        self._config_parser.read_file(
            codecs.open(PATH + "/conf/i18n_{0}.conf".format(Game().settings.language.code), "r", "utf-8"))

    def get(self, key: str) -> str:
        """Get the translation for the given key.

        :param key: The key of the translation.
        :return: The translated text.
        """

        return self._config_parser["TRANSLATIONS"][key]
