import json
from collections import defaultdict, deque

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from app import create_app, configure_app
from database.local_handler import LocalCSVDataInventory
from database.sql_handler import SqlDataInventory
from utility.build_schema import build_plotly_schema, build_schema
from utility.constants import *


def validate_config_data_references(config_dict):
    """
    Validates that
    1. config_dict is of form needed for Escalate OS
    2. all data source and column names references exist in the data
    :param config_dict:
    :return:
    """
    app = create_app()
    app = configure_app(app, config_dict)
    ctx = app.app_context()
    ctx.push()
    # handle code differently at two spots depending on whether we are dealing with file system or database
    csv_flag = config_dict[DATA_BACKEND] == LOCAL_CSV
    data_source_names = config_dict[DATA_SOURCES]
    data_inventory = LocalCSVDataInventory if csv_flag else SqlDataInventory
    data_source_names_found = data_inventory.get_available_data_source()
    try:
        # Checking if data source names are valid
        for index, data_source_name in enumerate(data_source_names):
            if data_source_name not in data_source_names_found:
                raise ValidationError(
                    "".join(
                        [
                            data_source_name,
                            " is an invalid data source name, needs to be one of [",
                            ", ".join(data_source_names_found),
                            "]",
                        ]
                    ),
                    path=deque([DATA_SOURCES, index]),
                )
        # put column names in format "data_source_name.column_name"
        possible_column_names = []
        for data_source_name in data_source_names:
            column_names = data_inventory.get_schema_for_data_source(data_source_name)
            possible_column_names.extend(
                [
                    ".".join(
                        [
                            data_source_name,
                            column_name if csv_flag else column_name.name,
                        ]
                    )
                    for column_name in column_names
                ]
            )

        schema = build_schema(data_source_names, possible_column_names)
        validate(instance=config_dict, schema=schema)
        print("Your config file is valid")
    except ValidationError as valid_error:
        print("The Config file is not valid:")
        print(valid_error.message)
        print("The error can be found in the config at:", list(valid_error.path))
    finally:
        ctx.pop()


if __name__ == "__main__":
    # todo: take this in as a command line argument
    config_file_path = "tests/test_data/test_app_local_handler_config.json"
    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)
    validate_config_data_references(config_dict)
