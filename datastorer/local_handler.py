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
    DATA_SOURCE_TYPE,
    DATA_FILE_PATH,
    LEFT_KEY,
    RIGHT_KEY,
)


def filter_operation(data_column, filter_dict):
    if filter_dict[SELECTOR_TYPE] == FILTER:
        entry_values_to_be_shown_in_plot = filter_dict[SELECTED]
        # data storers handle a single value different from multiple values
        if len(entry_values_to_be_shown_in_plot) > 1:
            return data_column.isin(entry_values_to_be_shown_in_plot)
        else:
            return data_column == entry_values_to_be_shown_in_plot[0]
    elif filter_dict[SELECTOR_TYPE] == NUMERICAL_FILTER:
        return OPERATIONS_FOR_NUMERICAL_FILTERS[filter_dict[OPERATION]](
            data_column, filter_dict[VALUE]
        )


class LocalCSVHandler(DataHandler):
    def __init__(self, data_sources):
        """
        :param data_sources: list of objects defining data files and join rules
        e.g., [{DATA_SOURCE_TYPE: "file_type_a"},
        {DATA_SOURCE_TYPE: "file_type_b",
        LEFT_KEY: "column_foo_in_file_type_a",
        RIGHT_KEY: "column_bar_in_file_type_b"}]
        """
        self.data_sources = data_sources
        for data_source in self.data_sources:
            data_source_name = data_source[DATA_SOURCE_TYPE]
            suffix = "{}*.csv" if data_source_name[-1] == "/" else "{}/*.csv"
            list_of_files = glob.glob(suffix.format(data_source_name))
            latest_filepath = max(list_of_files, key=os.path.getctime)
            data_source.update({DATA_FILE_PATH: latest_filepath})
        self.combined_data_table = self.build_combined_data_table()

    def build_combined_data_table(self):
        """
        Uses list of data sources to build a joined dataframe connecting related data
        todo: this is not likely changing very often, and may be slow to load
        Consider caching the data on a persistent LocalCSVHandler object instead of loading csvs and  merging every time we access the data
        :return: combined_data_table dataframe
        """
        combined_data_table = None
        # todo: join on multiple keys
        for data_source in self.data_sources:
            data_source_df = pd.read_csv(data_source[DATA_FILE_PATH])
            # the first data source defines the left most of any joins
            if combined_data_table is None:
                combined_data_table = data_source_df
            else:
                # left join the next data source to our combined data table
                combined_data_table = combined_data_table.merge(
                    data_source_df,
                    how="left",
                    left_on=LEFT_KEY,
                    right_on=RIGHT_KEY,
                    # add the data_source/table name as a suffix to new matching columns
                    suffixes=("", f"_{data_source[DATA_SOURCE_TYPE]}"),
                )
        return combined_data_table

    def get_column_names(self):
        return self.combined_data_table.tolist()

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
        df = self.combined_data_table[all_to_include_cols]
        for filter_dict in filters:
            df = df[filter_operation(df[filter_dict[OPTION_COL]], filter_dict)]

        return df[cols].to_dict("list")

    def get_column_unique_entries(self, cols: list) -> dict:
        unique_dict = {}
        for col in cols:
            # todo: note this assumption, we are dropping null values. I think we may want to be able to select them
            unique_dict[col] = self.combined_data_table[col].dropna().unique().tolist()
        return unique_dict
