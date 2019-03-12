from enum import Enum


class LanguageEnum(Enum):
    """List of the supported languages by the game.

    Each language must have a i18n_%ISO2_CODE%.conf defining the translations
    in the 'conf' folder.
    """

    ENGLISH = 0, "en"
    FRENCH = 1, "fr"

    def __init__(self, index, code):
        super().__init__()

        self._index = index
        self._code = code

    @property
    def index(self) -> int:
        """Get the index of the language.

        :return: The index of the language.
        """

        return self._index

    @property
    def code(self) -> str:
        """Get the ISO 2 code of the language.

        :return: The ISO 2 code of the language.
        """

        return self._code

    @staticmethod
    def from_index(index: int):
        """Get the language corresponding to this index.

        :param index: The index of the language.
        :return: A ``LanguageEnum``.
        """

        for i, language in enumerate(LanguageEnum):
            if i == index:
                return language

        return LanguageEnum.ENGLISH
