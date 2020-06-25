import pandas as pd
from sqlalchemy import inspect

from datastorer.data_handler import DataHandler
from datastorer.database import db_session


class SqlHandler(DataHandler):
    def __init__(self, table_name):
        module = __import__("datastorer.models", fromlist=[table_name])
        self.table_class = getattr(module, table_name)
        self.table = self.table_class.__table__

    # todo
    def build_combined_data_table(self):
        pass

    @staticmethod
    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    def get_column_names(self):
        """
        :return: a list of the column names in the table referenced by the handler
        """
        return list(self.table.columns.keys())

    def get_column_data(self, columns: list, filters: dict = None) -> dict:
        """
        :param columns: A complete list of the columns to be returned
        :param filters: Optional dict specifying how to filter the requested columns based on the row values
        :return: a dict keyed by column name and valued with lists of row datapoints for the column
        """
        # query = self.table_class.query
        query = db_session.query(*[getattr(self.table_class, col) for col in columns])
        raise NotImplementedError
        # todo: filter by inequality
        # Build the list of filters to apply to the data
        for filter_column, filter_value in filters.items():
            # filter is a single item, evaluate with sql's equality statement
            if isinstance(filter_value, (int, float, str)):
                query = query.filter(
                    getattr(self.table_class, filter_column) == filter_value
                )
            # filter is a list of possible items, evaluate with sql's "is in" statement
            elif isinstance(filter_value, (list, dict)):
                query = query.filter(
                    getattr(self.table_class, filter_column).in_(filter_value)
                )
        # response_rows is a list of tuples
        response_rows = query.all()
        # use pandas to read the sql response and convert to a dict of lists keyed by column names
        response_dict_of_lists = pd.DataFrame(response_rows).to_dict(orient="list")
        return response_dict_of_lists

    def get_column_unique_entries(self, cols: list) -> dict:
        """
        :param cols: a list of column names
        :return: A dict keyed by column names and valued with the unique values in that column
        """
        unique_dict = {}
        for col in cols:
            query = db_session.query(getattr(self.table_class, col)).distinct()
            response = query.all()
            # todo: note we're dropping none/missing values from the response. Do we want to be able to include them?
            unique_dict[col] = [r[0] for r in response if r[0] is not None]
        return unique_dict
