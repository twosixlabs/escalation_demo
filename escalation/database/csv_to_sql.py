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

from utility.constants import INDEX_COLUMN, UPLOAD_ID

DB_BACKEND = "psql"
if DB_BACKEND == "psql":
    from app_settings import PSQL_DATABASE_CONFIG as database_config
elif DB_BACKEND == "mysql":
    from app_settings import MYSQL_DATABASE_CONFIG as database_config

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

EXISTS_OPTIONS = ["replace", "append"]


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
                sqlalchemy_data_types.append(DATA_TYPE_MAP[tableschema_data_type])
            except KeyError:
                raise KeyError(
                    f"Mapping to sqlalchemy data type not found for {tableschema_data_type}"
                )
        return sqlalchemy_data_types

    @classmethod
    def create_new_table(
        cls, table_name, data, schema, key_columns=None, if_exists="replace"
    ):
        """Uses the Pandas sql connection to create a new table from CSV and generated schema."""
        # todo: don't hide warnings!
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # if there is no key specified, include the index
            index = key_columns is None
            if not index:
                # assign row numerical index to its own column
                data = data.reset_index()
            # add a data upload id and time column to all tables and
            data[UPLOAD_ID] = uuid.uuid1()
            if DB_BACKEND == "mysql":
                data.to_sql(
                    table_name,
                    con=cls.__engine,
                    schema=database_config["database"],
                    if_exists=if_exists,
                    chunksize=300,
                    dtype=schema,
                )
                # if we're creating this table new, build the pk
                if if_exists == "replace":
                    if key_columns:
                        cls.__engine.execute(
                            "ALTER TABLE {} ADD UNIQUE({}({}));".format(
                                table_name, *key_columns
                            )
                        )
                    else:
                        # use the numerical index from pandas as a pk
                        cls.__engine.execute(
                            f"ALTER TABLE {table_name} ADD UNIQUE({UPLOAD_ID}, {INDEX_COLUMN});"
                        )
            elif DB_BACKEND == "psql":
                if table_name.lower() != table_name:
                    raise ValueError(
                        "Postgres does not play well with upper cases in table names, please rename your table"
                    )
                data.to_sql(
                    table_name,
                    con=cls.__engine,
                    if_exists=if_exists,
                    chunksize=300,
                    dtype=schema,
                )
                # if we're creating this table new, build the pk
                if if_exists == "replace":
                    if key_columns:
                        cls.__engine.execute(
                            f"ALTER TABLE {table_name} add primary key (index_col[0]);"
                        )
                    else:
                        # use the numerical index from pandas as a pk
                        cls.__engine.execute(
                            f"ALTER TABLE {table_name} add primary key ({UPLOAD_ID}, {INDEX_COLUMN});"
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
    if_exists = sys.argv[3]
    assert if_exists in EXISTS_OPTIONS

    data = CreateTablesFromCSVs.get_data_from_csv(filepath)
    schema = CreateTablesFromCSVs.get_schema_from_csv(filepath)
    key_column = None

    CreateTablesFromCSVs.create_new_table(
        table_name, data, schema, key_columns=key_column, if_exists=if_exists
    )

    # example usage:
    # create a table in your db defined by a csv file
    # python database/csv_to_sql.py penguin_size /Users/nick.leiby/repos/escos/tests/test_data/penguin_size/penguin_size.csv
    # python database/csv_to_sql.py mean_penguin_stat /Users/nick.leiby/repos/escos/tests/test_data/mean_penguin_stat/mean_penguin_stat.csv

    # create a models.py file with the sqlalchemy model of the table
    # sqlacodegen postgresql+pg8000://escalation_os:escalation_os_pwd@localhost:54320/escalation_os --outfile database/models.py

# todo: add columns about upload time
# todo: add an upload metadata table if not exists that has upload time, user, id, numrows, etc from the submission
# todo: psql at least enforces lowercase table names- sanitize table names
# todo: write table create from schema and bulk insert the rows rather than using the pandas to_sql, which can be very slow
# todo: enforce no : in column or table names