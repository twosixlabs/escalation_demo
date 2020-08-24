# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0


import sys
from io import StringIO
import re

import pandas as pd
import psycopg2  # used here for fast copy_from performance
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.types import Integer, Text, DateTime, Float, Boolean
from tableschema import Table

from app_deploy_data.app_settings import DATABASE_CONFIG
from utility.constants import INDEX_COLUMN, UPLOAD_ID

DATA_TYPE_MAP = {
    "integer": Integer,
    "number": Float,
    "string": Text,
    "date": DateTime,
    "boolean": Boolean,
}

# # todo: bigger map:
# import sqlalchemy.types
#  decimal.Decimal: sqlalchemy.types.Numeric,
#  bytes: sqlalchemy.types.LargeBinary,
#  datetime.date: sqlalchemy.types.Date,
#  datetime.time: sqlalchemy.types.Time,
#  datetime.timedelta: sqlalchemy.types.Interval,
#  list: sqlalchemy.types.ARRAY,
#  dict: sqlalchemy.types.JSON

EXISTS_OPTIONS = ["replace", "append", "fail"]
POSTGRES_TABLE_NAME_FORMAT_REGEX = r"^[a-zA-Z_]\w+$"


def extract_values(obj, key):
    """Recursively pull values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Return all matching values in an object."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    if k == key:
                        arr.append(v)
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


class CreateTablesFromCSVs:
    """Infer a table schema from a CSV."""

    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def get_data_from_csv(csv_data_file_path):
        """
        :param csv_data_file_path:
        :return: pandas dataframe
        """
        return pd.read_csv(csv_data_file_path, encoding="utf-8", comment="#")

    @classmethod
    def get_schema_from_csv(cls, csv_data_file_path, confidence=0.05):
        """
        Infers schema from csv file, making predictions about data type and expressing the confidence in the predictions
        :param csv_data_file_path:
        :param confidence: ratio of casting errors allowed
        :return: schema_dict of names:data_types
        """
        table = Table(csv_data_file_path)
        table.infer(limit=500, confidence=confidence)
        schema = table.schema.descriptor
        # todo: we aren't evaluating the confidence failures here- what happens if we can't infer? UX step where the schema gets validated by a user?
        names = cls.get_column_names(schema, "name")
        datatypes = cls.get_column_datatypes(schema, "type")
        schema_dict = dict(zip(names, datatypes))
        return schema_dict

    @staticmethod
    def get_column_names(schema, key):
        """Get names of columns."""
        names = extract_values(schema, key)
        return names

    @staticmethod
    def get_column_datatypes(schema, key):
        """Convert python tableschema output to types to recognizable by SQLAlchemy."""
        tableschema_data_types = extract_values(schema, key)
        sqlalchemy_data_types = []
        for tableschema_data_type in tableschema_data_types:
            try:
                sqlalchemy_data_types.append(DATA_TYPE_MAP[tableschema_data_type])
            except KeyError:
                raise KeyError(
                    f"Mapping to sqlalchemy data type not found for {tableschema_data_type}"
                )
        return sqlalchemy_data_types

    @staticmethod
    def append_metadata_to_table(
        data, upload_id=None, key_columns=None,
    ):
        # if there is no key specified, include the index
        index = key_columns is not None
        if not index:
            # assign row numerical index to its own column
            data = data.reset_index()
            data.rename(columns={"index": INDEX_COLUMN}, inplace=True)
        # add a data upload id and time column to all tables and
        # todo: if we're not replacing, get a fresh id
        if upload_id is None:
            upload_id = 1
        data[UPLOAD_ID] = upload_id
        return data

    def create_new_table(
        self, table_name, data, schema, key_columns, if_exists="replace",
    ):
        """Uses the Pandas sql connection to create a new table from CSV and generated schema."""

        if table_name.lower() != table_name:
            # todo: make naming checks consistent with flask
            # https://docs.sqlalchemy.org/en/13/orm/extensions/automap.html
            raise ValueError(
                "Postgres does not play well with upper cases in table names, please rename your table"
            )

        if if_exists == "replace":
            data.head(0).to_sql(
                table_name,
                con=self.engine,
                dtype=schema,
                index=False,
                if_exists=if_exists,
            )
            # set up the primary keys for the table
            if key_columns:
                assert isinstance(key_columns, tuple)
                self.engine.execute(
                    f"ALTER TABLE {table_name} add primary key ({','.join([k for k in key_columns])});"
                )
            else:
                # use the numerical index from pandas as a pk
                self.engine.execute(
                    f"ALTER TABLE {table_name} add primary key ({UPLOAD_ID}, {INDEX_COLUMN});"
                )


def connect(db_config_dict):
    """ Connect to the PostgreSQL database server """
    config_dict = {
        k: v
        for k, v in db_config_dict.items()
        if k in ["host", "password", "database", "user"]
    }
    print(config_dict)
    try:
        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**config_dict)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
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
    try:
        # issues with separators here cause Error:  extra data after last expected column
        cursor.copy_expert(f"copy {table_name} from stdin (format csv)", buffer)
        conn.commit()
        print("Copying csv done")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
        return
    finally:
        cursor.close()


def write_and_fill_new_table_from_df(table_name, filepath_for_schema, data, if_exists):
    db_config = DATABASE_CONFIG
    connection_url = URL(**db_config)
    engine = create_engine(connection_url)
    sql_creator = CreateTablesFromCSVs(engine)

    schema = sql_creator.get_schema_from_csv(filepath_for_schema)
    key_column = None
    print(f"Creating empty table named {table_name}")
    data = sql_creator.append_metadata_to_table(data, key_columns=key_column)
    # this creates an empty table of the correct schema using pandas to_sql
    sql_creator.create_new_table(
        table_name, data, schema, key_columns=key_column, if_exists=if_exists
    )
    # bulk copy of the contents using psycopg2 copy_from, which is much faster, see:
    # https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
    psycopg2_config_dict = {
        "host": db_config["host"],
        "database": db_config["database"],
        "user": db_config["username"],
        "password": db_config["password"],
    }
    conn = connect(psycopg2_config_dict)
    psycopg2_copy_from_stringio(conn, data, table_name)


if __name__ == "__main__":
    """
    Create a table in your SQL db defined by a csv file. This is paired with sqlalchemy
    codegen to create entries in the model file for the table.

    example usage:
    python database/csv_to_sql.py penguin_size escalation/test_app_deploy_data/data/penguin_size/penguin_size.csv replace
    create a models.py file with the sqlalchemy models of the tables in the db
    sqlacodegen postgresql+pg8000://escalation_os:escalation_os_pwd@localhost:54320/escalation_os --outfile app_deploy_data/models.py
    Schema extraction inspired by:
    https://hackersandslackers.com/infer-datatypes-from-csvs-to-create/

    """
    table_name = sys.argv[1]
    filepath = sys.argv[2]
    if_exists = sys.argv[3]
    # todo - better arg handling with argparse or something
    assert if_exists in EXISTS_OPTIONS

    if not re.match(POSTGRES_TABLE_NAME_FORMAT_REGEX, table_name):
        print(
            "Table names name must start with a letter or an underscore;"
            " the rest of the string can contain letters, digits, and underscores."
        )
        exit(1)
    if len(table_name) > 31:
        print(
            "Postgres SQL only supports table names with length <= 31-"
            " additional characters will be ignored"
        )
        exit(1)
    if re.match("[A-Z]", table_name):
        print(
            "Postgres SQL table names are case insensitive- "
            "tablename will be converted to lowercase letters"
        )

    data = CreateTablesFromCSVs.get_data_from_csv(filepath)
    write_and_fill_new_table_from_df(table_name, filepath, data, if_exists)


# todo: add columns about upload time
