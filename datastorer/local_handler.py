from datastorer.data_handler import DataHandler
import pandas as pd
import glob
import os

class LocalHandler(DataHandler):
    def __init__(self, file_folder=None):
        suffix='{}*.csv' if file_folder[-1]=='/' else '{}/*.csv'
        list_of_files = glob.glob(suffix.format(file_folder))  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        self.file_path = latest_file

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
