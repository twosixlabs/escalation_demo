import pandas as pd
import glob
import os
from pathvalidate import sanitize_filename
from werkzeug.utils import secure_filename
from datetime import datetime

from flask import current_app
from database.data_handler import DataHandler
from database.utils import local_csv_handler_filter_operation
from utility.constants import (
    OPTION_COL,
    DATA_SOURCE_TYPE,
    DATA_LOCATION,
    JOIN_KEYS,
    DATA_FILE_DIRECTORY,
    APP_CONFIG_JSON,
    TABLE_COLUMN_SEPARATOR,
    SELECTED,
)


class LocalCSVHandler(DataHandler):
    def __init__(self, data_sources):
        """
        :param data_sources: list of objects defining data files and join rules
        e.g., [{DATA_SOURCE_TYPE: "file_type_a"},
        {DATA_SOURCE_TYPE: "file_type_b",
        JOIN_KEYS: [("column_foo_in_file_type_a", "column_bar_in_file_type_b"), (..., ...)]
        """
        self.data_sources = data_sources
        self.data_file_directory = current_app.config[APP_CONFIG_JSON][
            DATA_FILE_DIRECTORY
        ]
        for data_source in self.data_sources:
            filepaths_list = self.assemble_list_of_active_data_source_csvs(data_source)
            data_source.update({DATA_LOCATION: filepaths_list})
        self.combined_data_table = self.build_combined_data_table()

    def assemble_list_of_active_data_source_csvs(self, data_source):
        data_source_name = data_source[DATA_SOURCE_TYPE]
        data_source_subfolder = os.path.join(self.data_file_directory, data_source_name)
        filepaths_list = glob.glob(f"{data_source_subfolder}/*.csv")
        if data_source_name in current_app.config.active_data_source_filters:
            filepaths_list = current_app.config.active_data_source_filters[
                data_source_name
            ]
        assert len(filepaths_list) > 0
        return filepaths_list

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
            data_source_df = pd.concat(
                [pd.read_csv(filepath) for filepath in data_source[DATA_LOCATION]]
            )
            # add the data_source/table name as a prefix to disambiguate columns
            data_source_df = data_source_df.add_prefix(
                f"{data_source[DATA_SOURCE_TYPE]}{TABLE_COLUMN_SEPARATOR}"
            )
            # the first data source defines the leftmost of any joins
            if combined_data_table is None:
                combined_data_table = data_source_df
            else:
                left_keys, right_keys = zip(*data_source[JOIN_KEYS])
                # left join the next data source to our combined data table
                combined_data_table = combined_data_table.merge(
                    data_source_df, how="left", left_on=left_keys, right_on=right_keys,
                )
        return combined_data_table

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
        all_to_include_cols = set(cols + list(cols_for_filters))
        df = self.combined_data_table[all_to_include_cols]
        for filter_dict in filters:
            column = df[filter_dict[OPTION_COL]]
            df = df[local_csv_handler_filter_operation(column, filter_dict)]

        return df[cols]

    def get_column_unique_entries(self, cols: list) -> dict:
        unique_dict = {}
        for col in cols:
            # todo: note this assumption, we are dropping null values. I think we may want to be able to select them
            unique_dict[col] = (
                self.combined_data_table[col].astype(str).unique().tolist()
            )
        return unique_dict


class LocalCSVDataInventory(LocalCSVHandler):
    def __init__(self, data_sources):
        # Instance methods for this class refer to single data source table
        assert len(data_sources) == 1
        self.data_source_name = data_sources[0][DATA_SOURCE_TYPE]

    @staticmethod
    def get_available_data_sources():
        return [
            f.name
            for f in os.scandir(
                current_app.config[APP_CONFIG_JSON][DATA_FILE_DIRECTORY]
            )
            if f.is_dir()
        ]

    def get_identifiers_for_data_source(self):
        full_path = os.path.join(
            current_app.config[APP_CONFIG_JSON][DATA_FILE_DIRECTORY],
            self.data_source_name,
        )
        list_of_files = glob.glob(f"{full_path}/*.csv")
        assert len(list_of_files) > 0
        return list_of_files

    def get_schema_for_data_source(self):
        list_of_files = self.get_identifiers_for_data_source()
        latest_filepath = max(list_of_files, key=os.path.getctime)
        return pd.read_csv(latest_filepath, nrows=1).columns.tolist()

    def write_data_upload_to_backend(self, uploaded_data_df, file_name=None):
        """
        :param file_name:
        :param uploaded_data_df: pandas dataframe on which we have already done validation
        :param data_source_name:

        :return: Nothing
        """

        file_name = (
            datetime.utcnow().strftime("%Y%m%d-%H%M%S")
            if (file_name is None)
            else sanitize_filename(secure_filename(file_name))
        )
        file_name = (
            file_name if file_name.endswith(".csv") else "".join([file_name, ".csv"])
        )

        file_path = os.path.join(
            current_app.config[APP_CONFIG_JSON][DATA_FILE_DIRECTORY],
            self.data_source_name,
            file_name,
        )
        uploaded_data_df.to_csv(file_path)
