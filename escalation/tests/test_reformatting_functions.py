# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import copy
import json

import pytest
from werkzeug.datastructures import ImmutableMultiDict

from utility.constants import (
    AVAILABLE_PAGES,
    DATA,
    GRAPHIC_NUM,
    GRAPHICS,
    POINTS_NUM,
    SELECTABLE_DATA_LIST,
    SHOW_ALL_ROW,
    UPPER_INEQUALITY,
    VALUE,
    OPERATION,
    ACTIVE_SELECTORS,
    DATA_FILTERS,
)
from graphics.utils.reformatting_functions import (
    add_operations_to_the_data_from_addendum,
    add_active_selectors_to_selectable_data_list,
    add_instructions_to_config_dict,
)


@pytest.fixture()
def single_page_config_dict_and_addendum():
    config_file_path = "tests/test_data/test_app_local_handler_config.json"

    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)
    single_page_config_dict = copy.deepcopy(
        config_dict[AVAILABLE_PAGES]["penguins"][GRAPHICS]
    )
    addendum_dict = ImmutableMultiDict(
        [
            ("graphic_name", "graphic_0"),
            ("selection_0", "MALE"),
            ("selection_1", "Torgersen"),
            ("selection_1", "Dream"),
            ("selection_2_upper_operation", ">"),
            ("selection_2_upper_value", "4"),
            ("selection_2_lower_operation", ">="),
            ("selection_2_lower_value", ""),
        ]
    )

    return single_page_config_dict, addendum_dict


def test_add_active_selectors_to_selectable_data_list_with_addendum(
    single_page_config_dict_and_addendum,
):
    single_page_config_dict, addendum_dict = single_page_config_dict_and_addendum
    graphic_0_dict = single_page_config_dict["graphic_0"]
    add_active_selectors_to_selectable_data_list(
        graphic_0_dict[SELECTABLE_DATA_LIST], graphic_0_dict[DATA], addendum_dict
    )
    assert len(graphic_0_dict[SELECTABLE_DATA_LIST][0][ACTIVE_SELECTORS]) == 1
    assert "MALE" in graphic_0_dict[SELECTABLE_DATA_LIST][0][ACTIVE_SELECTORS]
    assert len(graphic_0_dict[SELECTABLE_DATA_LIST][1][ACTIVE_SELECTORS]) == 2
    assert "Torgersen" in graphic_0_dict[SELECTABLE_DATA_LIST][1][ACTIVE_SELECTORS]
    assert "Dream" in graphic_0_dict[SELECTABLE_DATA_LIST][1][ACTIVE_SELECTORS]
    assert (
        graphic_0_dict[SELECTABLE_DATA_LIST][2][ACTIVE_SELECTORS][UPPER_INEQUALITY][
            VALUE
        ]
        == "4"
    )
    assert (
        graphic_0_dict[SELECTABLE_DATA_LIST][2][ACTIVE_SELECTORS][UPPER_INEQUALITY][
            OPERATION
        ]
        == ">"
    )


def test_add_active_selectors_to_selectable_data_list_without_addendum(
    single_page_config_dict_and_addendum,
):
    single_page_config_dict, addendum_dict = single_page_config_dict_and_addendum
    graphic_0_dict = single_page_config_dict["graphic_0"]
    add_active_selectors_to_selectable_data_list(
        graphic_0_dict[SELECTABLE_DATA_LIST], graphic_0_dict[DATA], ImmutableMultiDict()
    )
    assert len(graphic_0_dict[SELECTABLE_DATA_LIST][0][ACTIVE_SELECTORS]) == 1
    assert SHOW_ALL_ROW in graphic_0_dict[SELECTABLE_DATA_LIST][0][ACTIVE_SELECTORS]
    assert len(graphic_0_dict[SELECTABLE_DATA_LIST][1][ACTIVE_SELECTORS]) == 1
    assert SHOW_ALL_ROW in graphic_0_dict[SELECTABLE_DATA_LIST][1][ACTIVE_SELECTORS]
    assert (
        graphic_0_dict[SELECTABLE_DATA_LIST][2][ACTIVE_SELECTORS][UPPER_INEQUALITY][
            VALUE
        ]
        == ""
    )
    assert (
        graphic_0_dict[SELECTABLE_DATA_LIST][2][ACTIVE_SELECTORS][UPPER_INEQUALITY][
            OPERATION
        ]
        == "<="
    )


def test_add_operations_to_the_data(single_page_config_dict_and_addendum):
    single_page_config_dict, addendum_dict = single_page_config_dict_and_addendum
    graphic_0_dict = single_page_config_dict["graphic_0"]
    operations_list = add_operations_to_the_data_from_addendum(
        graphic_0_dict[SELECTABLE_DATA_LIST], graphic_0_dict[DATA], addendum_dict
    )
    assert len(operations_list) == 3
    # TO DO break up
    assert operations_list[0] == {
        "type": "filter",
        "column": "penguin_size:sex",
        "selected": ["MALE"],
    }
    assert operations_list[1] == {
        "type": "filter",
        "column": "penguin_size:island",
        "selected": ["Torgersen", "Dream"],
    }
    assert operations_list[2] == {
        "type": "numerical_filter",
        "column": "penguin_size:culmen_length_mm",
        "operation": ">",
        "value": 4.0,
    }

    # test two

    graphic_1_dict = single_page_config_dict["graphic_1"]
    addendum_dict = ImmutableMultiDict(
        [("graphic_index", "graphic_1"), ("selection_0", "culmen_length_mm")]
    )

    operations_list = add_operations_to_the_data_from_addendum(
        graphic_1_dict[SELECTABLE_DATA_LIST], graphic_1_dict[DATA], addendum_dict
    )

    assert (
        single_page_config_dict[GRAPHIC_NUM.format(1)][DATA][POINTS_NUM.format(0)]["x"]
        == "culmen_length_mm"
    )


def test_add_instructions_to_config_dict(single_page_config_dict_and_addendum):
    single_page_config_dict, addendum_dict = single_page_config_dict_and_addendum
    single_page_config_dict_test = copy.deepcopy(single_page_config_dict)
    single_page_config_dict_test = add_instructions_to_config_dict(
        single_page_config_dict_test, None
    )
    # add instructions should call the other two methods which I am already testing for.
    # So I want to make sure it in actually doing something
    assert single_page_config_dict_test != single_page_config_dict
    assert DATA_FILTERS not in single_page_config_dict_test[GRAPHIC_NUM.format(0)]

    single_page_config_dict_test = copy.deepcopy(single_page_config_dict)
    single_page_config_dict_test = add_instructions_to_config_dict(
        single_page_config_dict_test, addendum_dict
    )
    assert DATA_FILTERS in single_page_config_dict_test[GRAPHIC_NUM.format(0)]


def test_add_instructions_to_config_dict_with_different_addendum(
    single_page_config_dict_and_addendum,
):
    single_page_config_dict, addendum_dict = single_page_config_dict_and_addendum
    single_page_config_dict_test = copy.deepcopy(single_page_config_dict)
    addendum_dict = ImmutableMultiDict(
        [
            ("graphic_name", "a_different_graph"),
            ("selection_0", "MALE"),
            ("selection_1", "Torgersen"),
            ("selection_1", "Dream"),
            ("selection_2_upper_operation", ">"),
            ("selection_2_upper_value", "4"),
            ("selection_2_lower_operation", ">="),
            ("selection_2_lower_value", ""),
        ]
    )
    single_page_config_dict_test = add_instructions_to_config_dict(
        single_page_config_dict_test, addendum_dict
    )
    graphic_0_dict = single_page_config_dict_test["graphic_0"]
    assert len(graphic_0_dict[SELECTABLE_DATA_LIST][0][ACTIVE_SELECTORS]) == 1
    assert SHOW_ALL_ROW in graphic_0_dict[SELECTABLE_DATA_LIST][0][ACTIVE_SELECTORS]
