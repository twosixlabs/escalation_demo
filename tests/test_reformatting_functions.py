import json

import pytest

from utility.constants import (
    AVAILABLE_PAGES,
    DATA,
    FILTERS,
    GRAPHIC_NUM,
    GRAPHICS,
    POINTS_NUM,
    DATA_FILTERS,
)
from utility.reformatting_functions import (
    add_info_from_addendum_to_config_dict,
    make_default_addendum,
)


@pytest.fixture()
def single_page_config_dict():
    config_file_path = "tests/test_data/test_app_local_handler_config.json"

    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)
    single_page_config_dict = config_dict[AVAILABLE_PAGES]["penguins"][GRAPHICS]
    return single_page_config_dict


def test_add_info_from_addendum_to_config_dict(single_page_config_dict):
    config_file_path = "tests/test_data/test_app_config_addendum.json"
    with open(config_file_path, "r") as config_file:
        addendum_dict = json.load(config_file)
    single_page_config_dict = add_info_from_addendum_to_config_dict(
        single_page_config_dict, addendum_dict
    )
    assert len(single_page_config_dict[GRAPHIC_NUM.format(0)][DATA_FILTERS]) == 3
    # TO DO break up
    assert single_page_config_dict[GRAPHIC_NUM.format(0)][DATA_FILTERS][0] == {
        "type": "filter",
        "column": "sex",
        "selected": "MALE",
        "list_of_values": False,
    }
    assert single_page_config_dict[GRAPHIC_NUM.format(0)][DATA_FILTERS][1] == {
        "type": "filter",
        "column": "island",
        "selected": ["Biscoe", "Dream"],
        "list_of_values": True,
    }
    assert single_page_config_dict[GRAPHIC_NUM.format(0)][DATA_FILTERS][2] == {
        "type": "numerical_filter",
        "column": "culmen_length_mm",
        "operation": "<=",
        "value": 4,
    }
    assert (
        single_page_config_dict[GRAPHIC_NUM.format(1)][DATA][POINTS_NUM.format(0)]["x"]
        == "culmen_length_mm"
    )


def test_make_default_addendum(single_page_config_dict):
    addendum_dict = make_default_addendum(single_page_config_dict)
    # TO DO fix this test
    assert addendum_dict == {
        "graphic_0": {
            "selection_0": {
                "type": "filter",
                "column": "sex",
                "selected": "SHOW_ALL_ROW",
            },
            "selection_1": {
                "type": "filter",
                "column": "island",
                "selected": "SHOW_ALL_ROW",
            },
            "selection_2": {
                "type": "numerical_filter",
                "column": "culmen_length_mm",
                "inequality_upper": {"operation": "<=", "value": None},
                "inequality_lower": {"operation": ">=", "value": None},
            },
        },
        "graphic_1": {
            "selection_0": {"type": "axis", "column": "x", "selected": "body_mass_g"}
        },
    }
