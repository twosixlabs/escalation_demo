from datastorer.data_handler import DataHandler
import pandas as pd


class LocalHandler(DataHandler):
    def __init__(self, file_path=None):
        self.file_path = file_path

    def get_column_names(self):
        return pd.read_csv(self.file_path, nrows=1).columns.tolist()

    def get_column_data(self, cols: list) -> list:
        """

        :param cols: list of str of the names of the columns of data you would like to plot
        :return: list of lists of the data
        """
        return pd.read_csv(self.file_path)[
            cols
        ].values.T.tolist()  # pulls out each column as a different list
