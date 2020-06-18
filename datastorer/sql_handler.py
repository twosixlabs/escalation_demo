from datastorer.data_handler import DataHandler
import pandas as pd


class SqlHandler(DataHandler):
    def __init__(self, table_name):
        super().__init__()
        self.engine = None
        self.table_name = table_name

    def get_column_names(self):
        raise NotImplementedError

    def get_column_data(self, data_dict: dict) -> dict:
        raise NotImplementedError
