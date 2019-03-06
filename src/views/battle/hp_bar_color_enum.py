from enum import Enum


class HPBarColorEnum(Enum):
    """Represents the list of colors the HP bar can take."""

    RED = "red", 20
    YELLOW = "yellow", 50
    GREEN = "green", 100

    def __init__(self, name: str, upper_limit: int) -> None:
        """Create a new HP bar color.

        :param name: The name of the color.
        :param upper_limit: The upper limit of the color.
        """

        super().__init__()
        self._name = name
        self._upper_limit = upper_limit

    @property
    def name(self) -> str:
        """Get the name of the color.

        :return: The name of the color.
        """

        return self._name

    @property
    def upper_limit(self) -> int:
        """Get the upper limit of the color.

        :return: The upper limit of the color.
        """

        return self._upper_limit
