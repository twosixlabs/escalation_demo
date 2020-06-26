from datastorer.data_handler import DataHandler
import pandas as pd
import glob
import os

from utility.available_selectors import OPERATIONS_FOR_NUMERICAL_FILTERS
from utility.constants import (
    FILTER,
    VALUE,
    NUMERICAL_FILTER,
    SELECTOR_TYPE,
    OPERATION,
    OPTION_COL,
    SELECTED,
    LIST_OF_VALUES,
)


def filter_operation(data_column, filter_dict):
    if filter_dict[SELECTOR_TYPE] == FILTER:
        entry_values_to_be_shown_in_plot = filter_dict[SELECTED]
        if filter_dict[LIST_OF_VALUES]:
            return data_column.isin(entry_values_to_be_shown_in_plot)
        else:
            return data_column == entry_values_to_be_shown_in_plot
    elif filter_dict[SELECTOR_TYPE] == NUMERICAL_FILTER:
        return OPERATIONS_FOR_NUMERICAL_FILTERS[filter_dict[OPERATION]](
            data_column, filter_dict[VALUE]
        )


class LocalCSVHandler(DataHandler):
    def __init__(self, file_folder=None):
        suffix = "{}*.csv" if file_folder[-1] == "/" else "{}/*.csv"
        list_of_files = glob.glob(suffix.format(file_folder))
        latest_file = max(list_of_files, key=os.path.getctime)
        self.file_path = latest_file

    def get_column_names(self):
        return pd.read_csv(self.file_path, nrows=1).columns.tolist()

    def get_column_data(self, cols: list, filters: list = None) -> dict:
        # error checking would be good
        """
        :param cols:
        :param filters:
        :return:
        """
        if filters is None:
            filters = []
        cols_for_filters = [filter_dict[OPTION_COL] for filter_dict in filters]
        all_to_include_cols = cols + list(cols_for_filters)
        df = pd.read_csv(self.file_path, usecols=all_to_include_cols)
        for filter_dict in filters:
            df = df[filter_operation(df[filter_dict[OPTION_COL]], filter_dict)]

        return df[cols].to_dict("list")

    def get_column_unique_entries(self, cols: list) -> dict:
        df = pd.read_csv(self.file_path)  # error checking will be good
        unique_dict = {}
        for col in cols:
            # todo: note this assumption, we are dropping null values. I think we may want to be able to select them
            unique_dict[col] = df[col].dropna().unique().tolist()
        return unique_dict
