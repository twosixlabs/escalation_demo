# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0
import os

from flask import current_app
import pandas as pd
import pytest
from sqlalchemy import create_engine, MetaData


from database.sql_handler import SqlDataInventory
from database.utils import sql_handler_filter_operation
from utility.constants import *
from tests.conftest import TESTING_DB_URI


@pytest.fixture()
def rebuild_test_database(test_app_client_sql_backed):
    # drop all tables assocatiated with the testing app Sqlalchemy Base
    engine = create_engine(TESTING_DB_URI)
    current_app.engine = engine
    current_app.Base.metadata.drop_all(bind=engine)
    current_app.Base.metadata.create_all(bind=engine)

    test_app_data_path = os.path.join(TEST_APP_DEPLOY_DATA, DATA)
    data_sources = os.listdir(test_app_data_path)
    for data_source in data_sources:
        if data_source == DATA_UPLOAD_METADATA:
            continue
        data_inventory = SqlDataInventory(
            data_sources={MAIN_DATA_SOURCE: {DATA_SOURCE_TYPE: data_source}}
        )
        data_source_path = os.path.join(test_app_data_path, data_source)
        files = os.listdir(data_source_path)
        for file in files:
            df = pd.read_csv(os.path.join(data_source_path, file), sep=",", comment="#")
            data_inventory.write_data_upload_to_backend(
                df, username="test_fixture", notes="test case upload"
            )
    return True


def test_sql_handler_get_column_names(rebuild_test_database):
    # todo: write this test and many others
    assert False


def test_sql_handler_filter_operation():
    # sql_handler_filter_operation(data_column, filter_dict)
    assert False


def test_get_class_name_from_table_name():
    assert False


def test_apply_filters_to_query():
    assert False


def test_build_combined_data_table():
    assert False


def test_get_column_data():
    assert False


def test_get_column_unique_entries():
    assert False


def test_build_filters_from_active_data_source():
    assert False


def test_sanitize_column_name():
    assert False


def test_data_frame_converter():
    assert False


def test_sql_data_inventory():
    assert False


def test_create_tables_from_csvs():
    assert False


def test_cast_dataframe_datatypes():
    assert False


def test_get_schema_from_df():
    assert False


def test_append_metadata_to_data():
    assert False


def test_get_available_data_sources():
    assert False


def test_write_upload_metadata_row():
    assert False


def test_get_new_upload_id_for_table():
    assert False


def test_get_schema_for_data_source():
    assert False


def test_write_data_upload_to_backend():
    assert False


def test_create_and_fill_new_sql_table_from_df():
    assert False


def test_get_data_from_csv():
    assert False


def test_create_new_table():
    assert False
