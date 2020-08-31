# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import json

from utility.constants import *


def load_config_file(config_file_path):
    with open(config_file_path, "r") as config_file:
        return json.load(config_file)


def get_data_inventory_class(csv_flag):
    if csv_flag:
        from database.local_handler import LocalCSVDataInventory

        data_inventory_class = LocalCSVDataInventory
    else:
        from database.sql_handler import SqlDataInventory

        data_inventory_class = SqlDataInventory
    return data_inventory_class


def get_possible_column_names(data_source_names, data_inventory_class, csv_flag):
    possible_column_names = []
    for data_source_name in data_source_names:
        data_inventory = data_inventory_class(
            data_sources={MAIN_DATA_SOURCE: {DATA_SOURCE_TYPE: data_source_name}}
        )
        column_names = data_inventory.get_schema_for_data_source()
        possible_column_names.extend(
            [
                TABLE_COLUMN_SEPARATOR.join(
                    [data_source_name, column_name if csv_flag else column_name.name,]
                )
                for column_name in column_names
            ]
        )
    return possible_column_names
