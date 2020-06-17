"""
Inspired by https://hackersandslackers.com/infer-datatypes-from-csvs-to-create/
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import pandas as pd
from tableschema import Table
from sqlalchemy.types import Integer, Text, Date, Numeric
import warnings

DATABASE_CONFIG = {
    'drivername': 'mysql+pymysql',
    'host': 'localhost',
    'port': '3306',
    'username': 'escalation_os_user',
    'password': 'escalation_os_pwd',
    'database': 'escalation_os'
}

DATA_TYPE_MAP = {'integer': Integer, 'number': Numeric, 'string': Text, 'date': Date}


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
    __engine = create_engine(URL(**DATABASE_CONFIG))

    @staticmethod
    def get_data_from_csv(csv_data_file_path):
        """
        :param csv_data_file_path:
        :return: pandas dataframe
        """
        return pd.read_csv(csv_data_file_path, encoding='utf-8')

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
        # import ipdb; ipdb.set_trace()
        names = cls.get_column_names(schema, 'name')
        datatypes = cls.get_column_datatypes(schema, 'type')
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
                raise KeyError(f"Mapping to sqlalchemy data type not found for {tableschema_data_type}")
        return sqlalchemy_data_types

    @classmethod
    def create_new_table(cls, data, schema):
        """Uses the Pandas sql connection to create a new table from CSV and generated schema."""
        # todo: don't hide warnings!
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            data.to_sql('faketable',
                        con=cls.__engine,
                        schema='escalation_os',
                        if_exists='replace',
                        chunksize=300,
                        dtype=schema)


if __name__ == '__main__':
    filepath = os.path.join('scratch', 'YeastSTATES-1-0-Growth-Curves__platereader.csv')
    data = CreateTablesFromCSVs.get_data_from_csv(filepath)
    schema = CreateTablesFromCSVs.get_schema_from_csv(filepath)
    print(f"Schema \n{schema}")
    CreateTablesFromCSVs.create_new_table(data, schema)
