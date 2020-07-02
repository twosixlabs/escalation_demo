import json

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from utility.build_schema import build_plotly_schema, build_schema

def get_data_names_from_table(config_file):
    pass

def validate_config_data_references(config_file):






if __name__ == "__main__":
    # todo: take this in as a command line argument
    config_file_path = "tests/test_data/test_sql_app_config.json"
    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)

    schema = build_schema()
    try:
        validate(instance=config_dict, schema=schema)


        print('Your config file is valid')
    except ValidationError as valid_error:
        print("The Config file is not valid:")
        print(valid_error.message)
        print(
            "The error can be found in the config at:", list(valid_error.absolute_path)
        )
