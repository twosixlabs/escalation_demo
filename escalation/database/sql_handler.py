# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0
from collections import OrderedDict
from datetime import datetime
import sys
from io import StringIO

from flask import current_app
import pandas as pd
import psycopg2  # used here for fast copy_from performance
from sqlalchemy import and_, func, create_engine, MetaData, Column, Table
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.types import (
    Integer,
    Text,
    DateTime,
    Float,
    Boolean,
    Date,
    JSON,
    Time,
    ARRAY,
    Interval,
)

from app_deploy_data.app_settings import DATABASE_CONFIG
from app_deploy_data.models import DataUploadMetadata
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
)


# from: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.types.infer_dtype.html
SQL_DATA_TYPE_MAP = {
    "integer": Integer,
    "floating": Float,
    "decimal": Float,
    "mixed-integer-float": Float,
    "string": Text,
    "mixed-integer": Text,
    "category": Text,
    "bytes": Text,
    "date": DateTime,
    "datetime64": DateTime,
    "datetime.date": Date,
    "time": Time,
    "timedelta64": Interval,
    "timedelta": Interval,
    "dict": JSON,
    "list": ARRAY,
    "boolean": Boolean,
}


REPLACE = "replace"
APPEND = "append"
FAIL = "fail"


def connect_to_db_using_psycopg2(db_config_dict):
    # bulk copy of the contents using psycopg2 copy_from, which is much faster, see:
    # https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/

    """ Connect to the PostgreSQL database server """
    psycopg2_config_dict = {
        "host": db_config_dict["host"],
        "database": db_config_dict["database"],
        "user": db_config_dict["username"],
        "password": db_config_dict["password"],
    }
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**psycopg2_config_dict)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    return conn


def psycopg2_copy_from_stringio(conn, df, table_name):
    """
    Here we are going save the dataframe in memory
    and use copy_from() to copy it to the table
    """
    # save dataframe to an in-memory buffer to use with copy_from, which requires fil
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    cursor = conn.cursor()
    # todo: assert that the column order matches expectation
    try:
        # issues with separators here cause Error: extra data after last expected column
        cursor.copy_expert(f"copy {table_name} from stdin (format csv)", buffer)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
        return False
    finally:
        cursor.close()


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
            if not filter_dict[SELECTED]:
                # No filter has been applied
                continue
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


class DataFrameConverter:
    """
    Shared helper methods that convert schemas between pandas and sql, alter data types,
    and add metadata to dataframes to match the expectations of the database.
    """

    @staticmethod
    def cast_dataframe_datatypes(data):
        def convert_to_nullable_int_if_able(x):
            # Pandas stores numerics with nulls as floats. Int64 (not int64) is nullable
            # Use this dtype where appropriate
            try:
                return x.astype("Int64")
            except TypeError:
                return x

        return data.apply(convert_to_nullable_int_if_able)

    @classmethod
    def get_schema_from_df(cls, data):
        """
        Infers schema from pandas df
        :return: schema_dict of names:data_types
        """

        data_cast = cls.cast_dataframe_datatypes(data)
        df_pandas_schema_dict = {}
        for column in data_cast.columns:
            df_pandas_schema_dict[column] = pd.api.types.infer_dtype(data_cast[column])
        df_sql_schema_dict = {
            k: SQL_DATA_TYPE_MAP[v] for k, v in df_pandas_schema_dict.items()
        }
        metadata_schema = OrderedDict({UPLOAD_ID: Integer, INDEX_COLUMN: Integer,})
        metadata_schema.update(df_sql_schema_dict)
        return data_cast, metadata_schema

    @staticmethod
    def append_metadata_to_data(data, upload_id, key_columns=None):
        """
        :param data: pandas df
        :param upload_id: integer upload id
        :param key_columns: user-specified primary key columns, if any
        :return: modified df with metadata columns
        """
        # if there is no key specified, include the index
        index = key_columns is not None
        if not index:
            # assign row numerical index to its own column
            data = data.reset_index()
            data.rename(columns={"index": INDEX_COLUMN}, inplace=True)
        # add upload_id and time column to the table at the first columns of the df
        data.insert(0, UPLOAD_ID, upload_id)
        return data


class SqlDataInventory(SqlHandler, DataFrameConverter):
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

    @staticmethod
    def write_upload_metadata_row(table_name, upload_time, upload_id, active=True):
        row = DataUploadMetadata(
            upload_id=upload_id,
            upload_time=upload_time,
            table_name=table_name,
            active=active,
        )
        db_session.add(row)
        db_session.commit()

    @staticmethod
    def get_new_upload_id_for_table(table_name):
        # get the max upload id currently associated with the table and increment it
        result = (
            db_session.query(func.max(DataUploadMetadata.upload_id))
            .filter(DataUploadMetadata.table_name == table_name)
            .first()
        )
        max_upload_id = result[0]  # always defined- tuple with None if no result
        # if there were no entries in the table for this upload ID, set default
        max_upload_id = max_upload_id or 0
        upload_id = max_upload_id + 1
        return upload_id

    def get_schema_for_data_source(self):
        """
        :param data_source_name: str
        :return: list of sqlalchemy column objects
        """
        return [c for c in self.table_lookup_by_name[self.data_source_name].columns]

    def write_data_upload_to_backend(self, uploaded_data_df):
        """
        :param uploaded_data_df: pandas dataframe on which we have already done validation
        :param data_source_name:
        Assumption: data_source for this upload is only one table, even though they can generally refer to more than one table

        :return:
        """
        uploaded_data_df = self.cast_dataframe_datatypes(uploaded_data_df)
        table = self.table_lookup_by_name[self.data_source_name]
        new_upload_id = self.get_new_upload_id_for_table(self.data_source_name)
        uploaded_data_df = self.append_metadata_to_data(
            data=uploaded_data_df, upload_id=new_upload_id
        )
        # todo: handle custom pk columns
        # # verify that all indices in the existing index column are unique
        # num_uploaded_rows = uploaded_data_df.shape[0]
        # num_unique_indexes = len(uploaded_data_df[INDEX_COLUMN].unique())
        # assert (
        #     num_unique_indexes == num_uploaded_rows
        # ), f"{INDEX_COLUMN} has non-unique values"

        # subset the columns to write to equal those in the db
        existing_columns = [c.name for c in table.columns]
        ignored_columns = set(uploaded_data_df.columns) - set(existing_columns)
        uploaded_data_df = uploaded_data_df[existing_columns]
        conn = connect_to_db_using_psycopg2(DATABASE_CONFIG)
        psycopg2_copy_from_stringio(conn, uploaded_data_df, self.data_source_name)
        upload_time = datetime.utcnow()
        self.write_upload_metadata_row(
            upload_time=upload_time,
            upload_id=new_upload_id,
            table_name=self.data_source_name,
            active=True,
        )
        return ignored_columns

    def write_new_data_file_type(self):
        """
        Handle the case where the user wants to upload a new data file type
        :return:
        """
        raise NotImplementedError


class CreateTablesFromCSVs(DataFrameConverter):
    """Infer a table schema from a CSV, and create a sql table from this definition"""

    def __init__(self, db_config):
        self.db_config = db_config
        connection_url = URL(**self.db_config)
        self.engine = create_engine(connection_url)
        self.reflect_db_tables_to_sqlalchemy_classes()
        self.Base = Base
        self.meta = MetaData(bind=self.engine)

    def create_and_fill_new_sql_table_from_df(self, table_name, data, if_exists):

        key_column = None
        print(f"Creating empty table named {table_name}")
        upload_id = SqlDataInventory.get_new_upload_id_for_table(table_name)
        upload_time = datetime.utcnow()
        data = self.append_metadata_to_data(
            data, upload_id=upload_id, key_columns=key_column,
        )
        data, schema = self.get_schema_from_df(data)
        # this creates an empty table of the correct schema using pandas to_sql
        self.create_new_table(
            table_name, schema, key_columns=key_column, if_exists=if_exists
        )

        conn = connect_to_db_using_psycopg2(self.db_config)
        success = psycopg2_copy_from_stringio(conn, data, table_name)
        if not success:
            raise Exception
        return upload_id, upload_time, table_name

    def reflect_db_tables_to_sqlalchemy_classes(self):
        self.Base = automap_base()
        # reflect the tables present in the sql database as sqlalchemy models
        self.Base.prepare(self.engine, reflect=True)

    @staticmethod
    def get_data_from_csv(csv_data_file_path):
        """
        :param csv_data_file_path:
        :return: pandas dataframe
        """
        return pd.read_csv(csv_data_file_path, encoding="utf-8", comment="#")

    def create_new_table(
        self, table_name, schema, key_columns, if_exists,
    ):
        """
        Create an EMPTY table from CSV and generated schema.
        Empty table because the ORM copy function is very slow- we'll populate the table
        data using a lower-level interface to SQL
        """

        self.meta.reflect()
        table_object = self.meta.tables.get(table_name)
        if table_object is not None:
            if if_exists == REPLACE:
                self.meta.drop_all(tables=[table_object])
                print(
                    f"Table {table_name} already exists- "
                    f"dropping and replacing as per argument"
                )
                self.meta.clear()
            elif if_exists == FAIL:
                raise KeyError(
                    f"Table {table_name} already exists- failing as per argument"
                )
            elif if_exists == APPEND:
                f"Table {table_name} already exists- appending data as per argument"
                return
        # table doesn't exist- create it
        columns = []
        primary_keys = key_columns or [UPLOAD_ID, INDEX_COLUMN]
        for name, sqlalchemy_dtype in schema.items():
            if name in primary_keys:
                columns.append(Column(name, sqlalchemy_dtype, primary_key=True))

            else:
                columns.append(Column(name, sqlalchemy_dtype))
        _ = Table(table_name, self.meta, *columns)
        self.meta.create_all()
