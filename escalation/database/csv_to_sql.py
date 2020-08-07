# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

"""
Inspired by https://hackersandslackers.com/infer-datatypes-from-csvs-to-create/
"""

import sys
import warnings
import uuid

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.types import Integer, Text, DateTime, Float, Boolean
from tableschema import Table

from app_deploy_data.app_settings import DATABASE_CONFIG
from utility.constants import INDEX_COLUMN, UPLOAD_ID, DATA_SOURCE_TYPE
from database.sql_handler import SqlDataInventory

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

    def __init__(self, database_config):
        self.database_config = database_config
        connection_url = URL(**database_config)
        self.engine = create_engine(connection_url)

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

    def create_new_table(
        self,
        table_name,
        data,
        schema,
        key_columns=None,
        if_exists="replace",
        upload_id=None,
    ):
        """Uses the Pandas sql connection to create a new table from CSV and generated schema."""
        # todo: don't hide warnings!
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
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

            if table_name.lower() != table_name:
                raise ValueError(
                    "Postgres does not play well with upper cases in table names, please rename your table"
                )
            data.head(0).to_sql(
                table_name,
                con=self.engine,
                if_exists=if_exists,
                dtype=schema,
                index=False,
            )

            if if_exists == "replace":
                if key_columns:
                    self.engine.execute(
                        f"ALTER TABLE {table_name} add primary key (index_col[0]);"
                    )
                else:
                    # use the numerical index from pandas as a pk
                    self.engine.execute(
                        f"ALTER TABLE {table_name} add primary key ({UPLOAD_ID}, {INDEX_COLUMN});"
                    )


def write_table(table_name, data):
    # todo: use automap
    # https: // docs.sqlalchemy.org / en / 13 / orm / extensions / automap.html
    # if the form of the submission is right, let's validate the content of the submitted file
    # data_inventory = SqlDataInventory(data_sources=[{DATA_SOURCE_TYPE: table_name}])
    # # write upload history table record at the same time
    # ignored_columns = data_inventory.write_data_upload_to_backend(data)
    return


if __name__ == "__main__":
    table_name = sys.argv[1]
    filepath = sys.argv[2]
    if_exists = sys.argv[3]
    assert if_exists in EXISTS_OPTIONS

    # DATABASE_CONFIG references host by Docker alias, but we're talking to the db from the host in this case
    db_config = DATABASE_CONFIG
    # db_config.update(
    #     {"host": "localhost",}
    # )
    sql_creator = CreateTablesFromCSVs(db_config)

    data = sql_creator.get_data_from_csv(filepath)
    schema = sql_creator.get_schema_from_csv(filepath)
    key_column = None
    # print(f"Creating table name {table_name} from file path {filepath}")
    # sql_creator.create_new_table(
    #     table_name, data, schema, key_columns=key_column, if_exists=if_exists
    # )
    write_table(table_name, data)

    # example usage:
    # create a table in your db defined by a csv file
    # python database/csv_to_sql.py penguin_size escalation/test_app_deploy_data/data/penguin_size/penguin_size.csv replace
    # python database/csv_to_sql.py mean_penguin_stat escalation/test_app_deploy_data/data/mean_penguin_stat/mean_penguin_stat.csv replace

    # create a models.py file with the sqlalchemy model of the table
    # sqlacodegen postgresql+pg8000://escalation_os:escalation_os_pwd@localhost:54320/escalation_os --outfile app_deploy_data/models.py

# todo: add columns about upload time
# todo: add an upload metadata table if not exists that has upload time, user, id, numrows, etc from the submission
# todo: psql at least enforces lowercase table names- sanitize table names
# todo: write table create from schema and bulk insert the rows rather than using the pandas to_sql, which can be very slow
# todo: enforce no : in column or table names
