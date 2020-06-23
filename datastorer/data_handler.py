from abc import ABC, abstractmethod


class DataHandler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_column_names(self) -> list:
        """
        :return: a list of the column names in the data source referenced by the handler
        """
        pass

    @abstractmethod
    def get_column_data(self, cols: list, filters: dict) -> list:
        """
        :param cols: list of column names, including all columns for which data should be returned
        :param filters: a dict keyed by column name and valued with the filters to be applied
        # todo: document the filtering allowed: equality, presence in list, inequality?
        :return: a dict keyed by column name and valued with lists of row datapoints for the column
        """
        pass

    @abstractmethod
    def get_column_unique_entries(self, cols: list) -> dict:
        """

        :param cols: list of column names
        :return: A dict keyed by column names and valued with the unique values in that column
        """
        pass
