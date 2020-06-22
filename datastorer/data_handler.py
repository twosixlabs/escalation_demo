from abc import ABC, abstractmethod


class DataHandler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_column_names(self):
        """
        What columns does the data have
        """
        pass

    @abstractmethod
    def get_column_data(self, cols: list) -> list:
        """

        :param cols: list of names
        :return:
        """
        pass

    @abstractmethod
    def get_column_unique_entries(self, cols: list) -> dict:
        """

        :param cols: list of names
        :return:
        """
        raise NotImplementedError
