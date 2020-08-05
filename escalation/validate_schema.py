# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import json
import os
from collections import deque

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from app import create_app, configure_app
from utility.build_schema import build_settings_schema, build_graphic_schema
from utility.constants import *


def load_config_file(config_file_path):
    with open(config_file_path, "r") as config_file:
        return json.load(config_file)


def get_data_inventory_class(csv_flag):
    if csv_flag:
        from escalation.database.local_handler import LocalCSVDataInventory

        data_inventory_class = LocalCSVDataInventory
    else:
        from escalation.database.sql_handler import SqlDataInventory

        data_inventory_class = SqlDataInventory
    return data_inventory_class


def get_possible_column_names(data_source_names, data_inventory_class, csv_flag):
    possible_column_names = []
    for data_source_name in data_source_names:
        data_inventory = data_inventory_class(
            data_sources=[{DATA_SOURCE_TYPE: data_source_name}]
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


def validate_config_data_references(config_dict_path):
    """
    Validates that
    1. config_dict is of form needed for Escalate OS
    2. all data source and column names references exist in the data
    :param config_dict:
    :return:
    """
    try:
        schema = build_settings_schema()
        current_config_path = config_dict_path
        config_dict = load_config_file(current_config_path)
        validate(instance=config_dict, schema=schema)
        app = create_app()
        app = configure_app(app, config_dict)
        ctx = app.app_context()
        ctx.push()
        # handle code differently at two spots depending on whether we are dealing with file system or database
        csv_flag = config_dict[DATA_BACKEND] == LOCAL_CSV
        data_source_names = config_dict[DATA_SOURCES]
        # data_backend_writer may be useful
        data_inventory_class = get_data_inventory_class(csv_flag)
        data_source_names_found = data_inventory_class.get_available_data_sources()

        # Checking if data source names are valid
        for index, data_source_name in enumerate(data_source_names):
            if data_source_name not in data_source_names_found:
                raise ValidationError(
                    f"{data_source_name} is an invalid data source name, needs to be"
                    f" one of [{', '.join(data_source_names_found)}].\nHave you added the data source as"
                    f" described in the setup instructions in README.md?",
                    path=deque(
                        [DATA_SOURCES, index]
                    ),  # jsonschema looking for a deque with the path to the error
                )

        possible_column_names = get_possible_column_names(
            data_source_names, data_inventory_class, csv_flag
        )
        # put column names in format "data_source_name.column_name"
        schema = build_graphic_schema(data_source_names, possible_column_names)

        pages = config_dict.get(AVAILABLE_PAGES, [])
        for page in pages:
            graphic_config_file_paths = page.get(GRAPHIC_CONFIG_FILES, [])
            for graphic_config_file_path in graphic_config_file_paths:
                current_config_path = os.path.join(
                    app.config[CONFIG_FILE_FOLDER], graphic_config_file_path
                )
                validate(instance=load_config_file(current_config_path), schema=schema)
        print("Your config file is valid")
    except ValidationError as valid_error:
        print("{} is not valid:".format(current_config_path))
        print(valid_error.message)
        print("The error can be found in the config at:", list(valid_error.path))


if __name__ == "__main__":
    # todo: take this in as a command line argument
    main_config_file_path = "test_app_deploy_data/test_app_local_config.json"
    validate_config_data_references(main_config_file_path)
