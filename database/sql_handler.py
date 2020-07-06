from datetime import datetime
import uuid

import pandas as pd
from sqlalchemy import and_

from database.data_handler import DataHandler
from database.database import db_session, Base
from database.utils import sql_handler_filter_operation
from utility.constants import (
    DATA_SOURCE_TYPE,
    DATA_LOCATION,
    UPLOAD_ID,
    OPTION_COL,
    INDEX_COLUMN,
    JOIN_KEYS,
    TABLE_COLUMN_SEPARATOR,
)


class SqlDataInventory:
    @staticmethod
    def get_available_data_source():
        # todo: intersect this with available sources in the config?
        return list(Base.metadata.tables.keys())

    @staticmethod
    def get_schema_for_data_source(data_source_name):
        """
        :param data_source_name: str
        :return: list of sqlalchemy column objects
        """
        table = Base.metadata.tables[data_source_name]
        schema_columns = table.columns.values()
        return schema_columns

    @staticmethod
    def get_sqlalchemy_model_class_for_data_source_name(data_source_name):
        """

        :param data_source_name:
        :return: sqlalchemy model class
        """
        for c in Base._decl_class_registry.values():
            if hasattr(c, "__tablename__") and c.__tablename__ == data_source_name:
                return c
        raise KeyError(f"{data_source_name} not found in available model classes")

    def write_data_upload_to_backend(self, uploaded_data_df, data_source_name):
        """
        :param uploaded_data_df: pandas dataframe on which we have already done validation
        :param data_source_name:
        Assumption: data_source for this upload is only one table, even though they can generally refer to more than one table

        :return:
        """
        sqlalchemy_model_class = self.get_sqlalchemy_model_class_for_data_source_name(
            data_source_name
        )
        table = sqlalchemy_model_class.__table__
        uploaded_data_df[UPLOAD_ID] = uuid.uuid1()
        # todo: write upload time and other upload information from the form to an uploads metadata table
        upload_time = datetime.utcnow()

        # if we are adding an index pk column, get it from the pandas df
        if INDEX_COLUMN in [c.name for c in table.primary_key]:
            if INDEX_COLUMN not in uploaded_data_df.columns:
                uploaded_data_df = uploaded_data_df.reset_index()
            else:
                # verify that all indices in the existing index column are unique
                num_uploaded_rows = uploaded_data_df.shape[0]
                num_unique_indexes = len(uploaded_data_df[INDEX_COLUMN].unique())
                assert (
                    num_unique_indexes == num_uploaded_rows
                ), f"{INDEX_COLUMN} has non-unique values"
        row_dicts_to_write = uploaded_data_df.to_dict("records")
        # todo: writing all of this to memory- could get gross for large uploads
        row_to_write = [sqlalchemy_model_class(**row) for row in row_dicts_to_write]
        db_session.bulk_save_objects(row_to_write)
        db_session.commit()
        return upload_time

    def write_new_data_file_type(self):
        """
        Handle the case where the user wants to upload a new data file type
        :return:
        """
        raise NotImplementedError


class SqlHandler(DataHandler):
    def __init__(self, data_sources):
        self.data_sources = data_sources
        self.table_lookup_by_name = {}
        for data_source in self.data_sources:
            table_name = data_source[DATA_SOURCE_TYPE]
            table_class = self.get_class_name_from_table_name(table_name)
            self.table_lookup_by_name[table_name] = table_class
            data_source.update({DATA_LOCATION: table_class})
        self.combined_data_table = self.build_combined_data_table()

    @staticmethod
    def get_class_name_from_table_name(table_name):
        """
        Camel-cased class name generated by sqlalchemy codegen doesn't match the sql table name. Fetch the class name based on matching class table name
        :param tablename str
        :return: table class object
        """
        return Base.metadata.tables[table_name]

    def build_combined_data_table(self):
        """
        This takes the tables specified in self.data_sources and combines them into one easily referenceable selectable.
        This is essentially a query view- performing the joins and getting all columns that can be filtered in a query.

        :return: SqlAlchemy DeclarativeMeta selectable class
        """
        # first build a query that will get all of the columns for all of the requested tables
        # look in current_ app for which takes and columns
        query = db_session.query(
            *[data_source[DATA_LOCATION] for data_source in self.data_sources]
        )
        for i, data_source in enumerate(self.data_sources):
            if i > 0:
                # sources after the first must have join information linking them to each other
                join_clauses = []
                for join_key_pair in data_source[JOIN_KEYS]:
                    left_table_name, left_column_name = join_key_pair[0].split(
                        TABLE_COLUMN_SEPARATOR
                    )
                    right_table_name, right_column_name = join_key_pair[1].split(
                        TABLE_COLUMN_SEPARATOR
                    )
                    left_table = self.table_lookup_by_name[left_table_name]
                    right_table = self.table_lookup_by_name[right_table_name]
                    join_clauses.append(
                        (
                            getattr(left_table.columns, left_column_name)
                            == getattr(right_table.columns, right_column_name)
                        )
                    )
                query = query.join(
                    data_source[DATA_LOCATION],
                    and_(*join_clauses),
                    # on clause matches corresponding table columns
                )

        # Dynamically defines the selectable class for the query view
        # This prefixes all column names with "{table_name}_"
        query_view_name = "_".join(
            [data_source[DATA_SOURCE_TYPE] for data_source in self.data_sources]
        )
        QueryView = type(
            query_view_name,  # name the class
            (Base,),  # inherit from Base
            {"__table__": query.selectable.alias()},  # give the class our selectable
        )
        return QueryView

    def get_column_names(self):
        """
        :return: a list of the column names in the table referenced by the handler
        """
        # todo: these are prefixed with table_name of the sub table in combined_data_table
        return list(self.combined_data_table().__table__.columns.keys())
        # raise NotImplementedError("This function is not used meaningfully, delete?")
        # return list(self.combined_data_table.columns.keys())

    @staticmethod
    def sanitize_column_name(column_name):
        # todo: better match how our auto schema is working to catch all rename logic
        return column_name.replace(TABLE_COLUMN_SEPARATOR, "_")

    def get_column_objects_from_config_string(self, columns):

        """
        rename is switching the '_' separation back to '.'
        Look up the right classes
        :return:
        """
        column_rename_dict = {
            self.sanitize_column_name(config_col): config_col for config_col in columns
        }
        column_mapping_dict = {
            config_col: getattr(self.combined_data_table, database_col)
            for database_col, config_col in column_rename_dict.items()
        }
        return column_rename_dict, column_mapping_dict

    def get_column_data(self, columns: list, filters: [] = None) -> dict:
        """
        :param columns: A complete list of the columns to be returned
        :param filters: Optional dict specifying how to filter the requested columns based on the row values
        :return: a dict keyed by column name and valued with lists of row datapoints for the column
        """
        if filters is None:
            filters = []
        cols_for_filters = [filter_dict[OPTION_COL] for filter_dict in filters]
        all_to_include_cols = list(set(columns + list(cols_for_filters)))

        (
            column_rename_dict,
            column_mapping_dict,
        ) = self.get_column_objects_from_config_string(all_to_include_cols)
        # build basic query requesting all of the columns needed
        query = db_session.query(*column_mapping_dict.values())
        # add filters to the query dynamically
        filter_tuples = []
        for filter_dict in filters:
            column_object = column_mapping_dict[filter_dict[OPTION_COL]]
            filter_tuples.append(
                sql_handler_filter_operation(column_object, filter_dict)
            )
        if filter_tuples:
            query = query.filter(*filter_tuples)

        response_rows = query.all()
        if response_rows:
            # use pandas to read the sql response and convert to a dict of lists keyed by column names
            # rename is switching the '_' separation back to '.'
            response_as_df = pd.DataFrame(response_rows).rename(
                columns=column_rename_dict
            )
        else:
            # if the sql query returns no rows, we want an empty df to format our response
            response_as_df = pd.DataFrame(columns=columns)
        response_dict_of_lists = response_as_df[columns].to_dict(orient="list")
        return response_dict_of_lists

    def get_column_unique_entries(self, cols: list) -> dict:
        """
        :param cols: a list of column names
        :return: A dict keyed by column names and valued with the unique values in that column
        """
        unique_dict = {}
        (
            column_rename_dict,
            column_mapping_dict,
        ) = self.get_column_objects_from_config_string(cols)
        for config_col, sql_col_class in column_mapping_dict.items():
            query = db_session.query(sql_col_class).distinct()
            response = query.all()
            unique_dict[config_col] = [r[0] for r in response]
        return unique_dict
