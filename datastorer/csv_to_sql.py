"""
Inspired by https://hackersandslackers.com/infer-datatypes-from-csvs-to-create/
"""

import os
import sys
import warnings

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.types import Integer, Text, Date, Float
from tableschema import Table

DB_BACKEND = "psql"
if DB_BACKEND == "psql":
    from app_settings import PSQL_DATABASE_CONFIG as database_config
elif DB_BACKEND == "mysql":
    from app_settings import MYSQL_DATABASE_CONFIG as database_config

DATA_TYPE_MAP = {"integer": Integer, "number": Float, "string": Text, "date": Date}


# todo: bigger map:
# int: sqlalchemy.sql.sqltypes.BigInteger,
#  str: sqlalchemy.sql.sqltypes.Unicode,
#  float: sqlalchemy.sql.sqltypes.Float,
#  decimal.Decimal: sqlalchemy.sql.sqltypes.Numeric,
#  datetime.datetime: sqlalchemy.sql.sqltypes.DateTime,
#  bytes: sqlalchemy.sql.sqltypes.LargeBinary,
#  bool: sqlalchemy.sql.sqltypes.Boolean,
#  datetime.date: sqlalchemy.sql.sqltypes.Date,
#  datetime.time: sqlalchemy.sql.sqltypes.Time,
#  datetime.timedelta: sqlalchemy.sql.sqltypes.Interval,
#  list: sqlalchemy.sql.sqltypes.ARRAY,
#  dict: sqlalchemy.sql.sqltypes.JSON


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

    connection_url = URL(**database_config)
    print(connection_url)
    __engine = create_engine(connection_url)

    @staticmethod
    def get_data_from_csv(csv_data_file_path):
        """
        :param csv_data_file_path:
        :return: pandas dataframe
        """
        return pd.read_csv(csv_data_file_path, encoding="utf-8")

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
                sqlalchemy_data_types.append(DATA_TYPE_MAP.get(tableschema_data_type))
            except KeyError:
                raise KeyError(
                    f"Mapping to sqlalchemy data type not found for {tableschema_data_type}"
                )
        return sqlalchemy_data_types

    @classmethod
    def create_new_table(cls, table_name, data, schema, key_columns=None):
        """Uses the Pandas sql connection to create a new table from CSV and generated schema."""
        # todo: don't hide warnings!
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # if there is no key specified, include the index
            index = key_columns is None
            if DB_BACKEND == "mysql":
                data.to_sql(
                    table_name,
                    con=cls.__engine,
                    schema=database_config["database"],
                    if_exists="replace",
                    chunksize=300,
                    dtype=schema,
                    index=index,
                )
                if key_columns:
                    cls.__engine.execute(
                        "ALTER TABLE {} ADD UNIQUE({}({}));".format(
                            table_name, *key_columns
                        )
                    )
                else:
                    # use the numerical index from pandas as a pk
                    cls.__engine.execute(
                        "ALTER TABLE {} ADD UNIQUE({});".format(table_name, "index")
                    )
            elif DB_BACKEND == "psql":
                data.to_sql(
                    table_name,
                    con=cls.__engine,
                    if_exists="replace",
                    chunksize=300,
                    dtype=schema,
                    index=index,
                )
                if key_columns:
                    cls.__engine.execute(
                        f"ALTER TABLE {table_name} add primary key (index_col[0]);"
                    )
                else:
                    # use the numerical index from pandas as a pk
                    cls.__engine.execute(
                        f"ALTER TABLE {table_name} add primary key (index);"
                    )


if __name__ == "__main__":
    # filepath = os.path.join("scratch", "YeastSTATES-1-0-Growth-Curves__platereader.csv")
    # data = CreateTablesFromCSVs.get_data_from_csv(filepath)
    # schema = CreateTablesFromCSVs.get_schema_from_csv(filepath)
    # table_name = "platereader"
    # # index_cols = [col_name for col_name in schema if 'id' in col_name.lower()]
    # index_col = (
    #     "_id",
    #     24,
    # )  # we need a way of determining for text columns used as ids the max length
    # CreateTablesFromCSVs.create_new_table(table_name, data, schema, index_col=index_col)
    # sqlacodegen mysql+pymysql://escalation_os_user:escalation_os_pwd@localhost:3306/escalation_os --outfile datastorer/models.py

    table_name = sys.argv[1]
    filepath = sys.argv[2]
    data = CreateTablesFromCSVs.get_data_from_csv(filepath)
    schema = CreateTablesFromCSVs.get_schema_from_csv(filepath)
    key_column = None
    CreateTablesFromCSVs.create_new_table(
        table_name, data, schema, key_columns=key_column
    )

    # example usage:
    # create a table in your db defined by a csv file
    # python datastorer/csv_to_sql.py penguin_size /Users/nick.leiby/repos/escos/tests/test_data/penguins_size/penguins_size.csv
    # create a models.py file with the sqlalchemy model of the table
    # sqlacodegen postgresql+pg8000://escalation_os:escalation_os_pwd@localhost:54320/escalation_os --outfile datastorer/models.py

# todo: add columns about upload time, upload id, to df and to sql. How are we choosing which data to show in our later queries?
