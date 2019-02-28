from configparser import ConfigParser

from toolbox.singleton import Singleton


class I18n(metaclass=Singleton):
    """Helps to manage internationalization."""

    def __init__(self):
        self._config_parser = ConfigParser()
        self._config_parser.read("../conf/i18n_en.conf")

    def get(self, key):
        return self._config_parser["TRANSLATIONS"][key]
