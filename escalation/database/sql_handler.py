# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

from flask import current_app
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
    OPTION_TYPE,
    FILTER,
    SELECTED,
    UNFILTERED_SELECTOR,
    COLUMN_NAME,
    MAIN_DATA_SOURCE,
    ADDITIONAL_DATA_SOURCES,
    APP_CONFIG_JSON,
    DATA_SOURCES,
)


class SqlHandler(DataHandler):
    def __init__(self, data_sources):
        self.data_sources = data_sources
        self.table_lookup_by_name = {}
        # create a flattened list from the data_sources object
        self.flat_data_sources = [
            self.data_sources[MAIN_DATA_SOURCE]
        ] + self.data_sources.get(ADDITIONAL_DATA_SOURCES, [])
        for data_source in self.flat_data_sources:
            table_name = data_source[DATA_SOURCE_TYPE]
            table_class = self.get_class_name_from_table_name(table_name)
            self.table_lookup_by_name[table_name] = table_class
            data_source.update({DATA_LOCATION: table_class})
        self.column_lookup_by_name = self.build_combined_data_table()

    @staticmethod
    def get_class_name_from_table_name(table_name):
        """
        Camel-cased class name generated by sqlalchemy codegen doesn't match the sql table name. Fetch the class name based on matching class table name
        :param tablename str
        :return: table class object
        """
        return Base.metadata.tables[table_name]

    def apply_filters_to_query(self, query, filters):
        # add filters to the query dynamically
        filter_tuples = []
        for filter_dict in filters:
            column_name = self.sanitize_column_name(filter_dict[OPTION_COL])
            column_object = self.column_lookup_by_name[column_name]
            filter_tuples.append(
                sql_handler_filter_operation(column_object, filter_dict)
            )
        if filter_tuples:
            query = query.filter(*filter_tuples)
        return query

    def build_combined_data_table(self):
        """
        This takes the tables specified in self.data_sources and combines them into one easily referenceable selectable.
        This is essentially a query view- performing the joins and getting all columns that can be filtered in a query.

        :return: dictionary keyed by column names and valued with SqlAlchemy column objects
        """
        # first build a query that will get all of the columns for all of active data in the requested tables
        query = db_session.query(*list(self.table_lookup_by_name.values()))
        # specify how the different data sources are joined
        for data_source in self.data_sources.get(ADDITIONAL_DATA_SOURCES, []):
            join_clauses = []
            for left_join_key, right_join_key in data_source[JOIN_KEYS]:
                left_table_name, left_column_name = left_join_key.split(
                    TABLE_COLUMN_SEPARATOR
                )
                right_table_name, right_column_name = right_join_key.split(
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
            query = query.join(data_source[DATA_LOCATION], and_(*join_clauses))

        column_lookup_by_name = {c.name: c for c in query.selectable.alias().columns}
        return column_lookup_by_name

    def build_filters_from_active_data_source(self):
        current_tables = list(self.table_lookup_by_name.keys())
        active_data_source_filters = []
        for (
            table_name,
            upload_ids,
        ) in current_app.config.active_data_source_filters.items():
            if table_name in current_tables:
                active_data_source_filters.append(
                    {
                        OPTION_TYPE: FILTER,
                        OPTION_COL: f"{table_name}:{UPLOAD_ID}",
                        SELECTED: upload_ids,
                    }
                )
        return active_data_source_filters

    @staticmethod
    def sanitize_column_name(column_name):
        # todo: better match how our auto schema is working to catch all rename logic
        return column_name.replace(TABLE_COLUMN_SEPARATOR, "_")

    def get_column_data(self, columns: list, filters: [] = None) -> dict:
        """
        :param columns: A complete list of the columns to be returned
        :param filters: Optional list specifying how to filter the requested columns based on the row values
        :return: a dict keyed by column name and valued with lists of row datapoints for the column
        """
        # import ipdb; ipdb.set_trace()
        if filters is None:
            filters = []
        cols_for_filters = [filter_dict[OPTION_COL] for filter_dict in filters]
        all_to_include_cols = list(set(columns + list(cols_for_filters)))
        all_column_rename_dict = {
            self.sanitize_column_name(c): c for c in all_to_include_cols
        }
        # build basic query requesting all of the columns needed
        query = db_session.query(
            *[self.column_lookup_by_name[c] for c in all_column_rename_dict.keys()]
        )
        active_data_filters = self.build_filters_from_active_data_source()
        filters.extend(active_data_filters)
        query = self.apply_filters_to_query(query, filters)
        response_rows = query.all()
        if response_rows:
            # rename is switching the '_' separation back to TABLE_COLUMN_SEPARATOR
            response_as_df = pd.DataFrame(response_rows).rename(
                columns=all_column_rename_dict
            )
        else:
            # if the sql query returns no rows, we want an empty df to format our response
            response_as_df = pd.DataFrame(columns=columns)
        return response_as_df[columns]

    def get_column_unique_entries(
        self, cols: list, filter_active_data=True, filters: list = None
    ) -> dict:
        """
        :param cols: a list of column names
        :param filters: Optional list specifying how to filter the requested columns based on the row values
        :param filter_active_data: Whether to filter the column entries to only include those for active data sources
        :return: A dict keyed by column names and valued with the unique values in that column
        """
        if filters is None:
            filters = []
        unique_dict = {}
        for col in cols:
            renamed_col = self.sanitize_column_name(col)
            sql_col_class = self.column_lookup_by_name[renamed_col]
            query = db_session.query(sql_col_class).distinct()
            if filter_active_data:
                active_data_filters = self.build_filters_from_active_data_source()
                query = self.apply_filters_to_query(query, active_data_filters)
            # if the current column matches one in the filter list marked as unfiltered,
            # skip this and don't apply the filters before looking for unique values
            if not any(
                [
                    (filter_[COLUMN_NAME] == col and filter_.get(UNFILTERED_SELECTOR))
                    for filter_ in filters
                ]
            ):
                query = self.apply_filters_to_query(query, filters)
            response = query.all()
            unique_dict[col] = [str(r[0]) for r in response if r[0] is not None]
        return unique_dict


class SqlDataInventory(SqlHandler):
    def __init__(self, data_sources):
        # Instance methods for this class refer to single data source table
        assert len(data_sources) == 1
        super().__init__(data_sources)
        self.data_source_name = [*self.table_lookup_by_name.keys()][0]

    @staticmethod
    def get_available_data_sources():
        """
        Lists all data sources available in the db
        :return:
        """
        return [table_name for table_name in Base.metadata.tables.keys()]

    def get_identifiers_for_data_source(self):
        """
        :return: List of upload_id identifiers for the table source
        """
        upload_id_column = TABLE_COLUMN_SEPARATOR.join(
            [self.data_source_name, UPLOAD_ID]
        )
        return self.get_column_unique_entries(
            cols=[upload_id_column], filter_active_data=False
        )[upload_id_column]

    def get_schema_for_data_source(self):
        """
        :param data_source_name: str
        :return: list of sqlalchemy column objects
        """
        return [c for c in self.table_lookup_by_name[self.data_source_name].columns]

    def get_sqlalchemy_model_class_for_data_source_name(self):
        """
        :param data_source_name:
        :return: sqlalchemy model class
        """
        for c in Base._decl_class_registry.values():
            if hasattr(c, "__tablename__") and c.__tablename__ == self.data_source_name:
                return c
        raise KeyError(f"{self.data_source_name} not found in available model classes")

    def write_data_upload_to_backend(self, uploaded_data_df):
        """
        :param uploaded_data_df: pandas dataframe on which we have already done validation
        :param data_source_name:
        Assumption: data_source for this upload is only one table, even though they can generally refer to more than one table

        :return:
        """
        sqlalchemy_model_class = self.get_sqlalchemy_model_class_for_data_source_name()
        table = self.table_lookup_by_name[self.data_source_name]
        existing_upload_ids = self.get_identifiers_for_data_source()
        # todo: getting the id this way is sloppy- it's a race condition
        new_upload_id = int(max(existing_upload_ids) + 1)
        uploaded_data_df[UPLOAD_ID] = new_upload_id
        # todo: write upload time and other upload information from the form to an uploads metadata table
        # upload_time = datetime.utcnow()

        # if we are adding an index pk column, get it from the pandas df
        if INDEX_COLUMN in [c.name for c in table.primary_key]:
            if INDEX_COLUMN not in uploaded_data_df.columns:
                uploaded_data_df.index.rename(INDEX_COLUMN, inplace=True)
                uploaded_data_df.reset_index(inplace=True)
            else:
                # verify that all indices in the existing index column are unique
                num_uploaded_rows = uploaded_data_df.shape[0]
                num_unique_indexes = len(uploaded_data_df[INDEX_COLUMN].unique())
                assert (
                    num_unique_indexes == num_uploaded_rows
                ), f"{INDEX_COLUMN} has non-unique values"

        # subset the columns to write to equal those in the db
        existing_columns = {c.name for c in table.columns}
        ignored_columns = set(uploaded_data_df.columns) - existing_columns
        uploaded_data_df = uploaded_data_df[existing_columns]
        # todo: columns in the sqlalchemy_model_class are attributes auto-names by sqlalchemy codegen, and have some character replacement
        # how do we build the right inserts here?
        rename_dict = {
            k: k.replace("-", "_").replace("/", "_") for k in uploaded_data_df.columns
        }
        uploaded_data_df.rename(columns=rename_dict, inplace=True)
        row_dicts_to_write = uploaded_data_df.to_dict("records")
        # todo: writing all of this to memory- could get gross for large uploads
        row_to_write = [sqlalchemy_model_class(**row) for row in row_dicts_to_write]
        db_session.bulk_save_objects(row_to_write)
        db_session.commit()
        return ignored_columns

    def write_new_data_file_type(self):
        """
        Handle the case where the user wants to upload a new data file type
        :return:
        """
        raise NotImplementedError
