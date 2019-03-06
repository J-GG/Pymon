from configparser import ConfigParser

from toolbox.init import PATH
from toolbox.singleton import Singleton


class I18n(metaclass=Singleton):
    """Helps to manage internationalization."""

    def __init__(self):
        """Create a new object to manage internationalization."""

        self._config_parser = ConfigParser()
        self._config_parser.read(PATH + "/conf/i18n_en.conf")

    def get(self, key: str) -> str:
        """Get the translation for the given key.

        :param key: The key of the translation.
        :return: The translated text.
        """

        return self._config_parser["TRANSLATIONS"][key]
