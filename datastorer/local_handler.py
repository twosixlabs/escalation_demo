from datastorer.data_handler import DataHandler
import pandas as pd


class LocalHandler(DataHandler):
    def __init__(self, file_path=None):
        super().__init__()
        self.file_path = file_path

    def get_columns_names(self):
        return pd.read_csv(self.file_path, nrows=1).columns.tolist()

    def get_column_data(self, cols: list) -> list:
        return super().get_column_data(cols)
