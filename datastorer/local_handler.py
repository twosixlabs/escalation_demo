from datastorer.data_handler import DataHandler
import pandas as pd


class LocalHandler(DataHandler):
    def __init__(self, file_path=None):
        self.file_path = file_path

    def get_column_names(self):
        return pd.read_csv(self.file_path, nrows=1).columns.tolist()

    def get_column_data(self, data_dict: dict) -> dict:
        """
        :param cols:
        :return:
        """
        df = pd.read_csv(self.file_path)
        for key, column in data_dict.items():
            data_dict[key] = df[column].values

        return data_dict
