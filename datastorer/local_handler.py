from datastorer.data_handler import DataHandler
import pandas as pd
import glob
import os


class LocalCSVHandler(DataHandler):
    def __init__(self, file_folder=None):
        suffix = "{}*.csv" if file_folder[-1] == "/" else "{}/*.csv"
        list_of_files = glob.glob(suffix.format(file_folder))
        latest_file = max(list_of_files, key=os.path.getctime)
        self.file_path = latest_file

    def get_column_names(self):
        return pd.read_csv(self.file_path, nrows=1).columns.tolist()

    def get_column_data(self, cols: list, filters: dict = None) -> dict:
        # error checking will be good
        """
        :param cols:
        :param filters:
        :return:
        """
        if filters is None:
            filters = {}
        all_to_include_cols = cols + list(filters)
        df = pd.read_csv(self.file_path, usecols=all_to_include_cols)
        for column_name, entry_values_to_be_shown_in_plot in filters.items():
            df = df[df[column_name].isin(entry_values_to_be_shown_in_plot)]
        # return df[cols].to_dict("list")

        return df[cols]

    def get_column_unique_entries(self, cols: list) -> dict:
        df = pd.read_csv(self.file_path)  # error checking will be good
        unique_dict = {}
        for col in cols:
            # todo: note this assumption, we are dropping null values. I think we may want to be able to select them
            unique_dict[col] = df[col].dropna().unique().tolist()
        return unique_dict
