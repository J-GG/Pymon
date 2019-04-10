import os
import typing

import dill

from toolbox.init import PATH


class Persistence:
    """Manages the persistence of the models.

    Attributes:
        - DATA_PATH: Folder containing the serialized data. is created if it
        doesn't exist.
        - FILE_NAME: Name of the file containing the data of the model.
    """

    DATA_PATH = PATH + "/data/"

    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    FILE_NAME = ""

    def save(self) -> None:
        """Save the model into a file."""

        with open(Persistence.DATA_PATH + self.FILE_NAME, 'w+b') as file:
            dill.dump(self, file)

    @classmethod
    def load(cls) -> typing.Union[typing.Any, None]:
        """Load the model file.

        :return The deserialized model.
        """

        if os.path.isfile(Persistence.DATA_PATH + cls.FILE_NAME):
            with open(Persistence.DATA_PATH + cls.FILE_NAME, "rb") as file:
                deserialized_model = dill.load(file)
                return deserialized_model
        else:
            return cls()

    @classmethod
    def delete(cls) -> None:
        """Remove the file."""

        if os.path.isfile(Persistence.DATA_PATH + cls.FILE_NAME):
            os.remove(Persistence.DATA_PATH + cls.FILE_NAME)
