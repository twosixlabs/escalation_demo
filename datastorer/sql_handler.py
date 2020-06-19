from sqlalchemy import inspect

from datastorer.data_handler import DataHandler
from datastorer.database import db_session


class SqlHandler(DataHandler):
    def __init__(self, table_name):
        module = __import__("datastorer.models", fromlist=[table_name])
        self.table_class = getattr(module, table_name)
        self.table = self.table_class.__table__

    @staticmethod
    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    def get_column_names(self):
        return list(self.table.columns.keys())

    def get_column_data(self, data_dict: dict) -> dict:
        query = self.table_class.query
        # Build the list of filters to apply to the data
        for filter_column, filter_value in data_dict.items():
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
        response = query.all()
        # todo: we're not filtering the columns queried here, and I'm overloading the data_dict input. We need additional filtering logic here as a filter arg, I think
        # the orm query from above doesn't allow easy parsing.
        # db_session.query(sql_handler.table_class.od).first()._asdict()
        # todo: response to dict
        return [self.object_as_dict(x) for x in response]
