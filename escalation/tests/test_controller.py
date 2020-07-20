# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

from collections import OrderedDict

from controller import (
    create_link_buttons_for_available_pages,
    create_data_subselect_info_for_plot,
    get_unique_set_of_columns_needed,
    get_data_selection_info_for_page_render,
    remove_redundant_filters_from_active_selectors,
)
from database.utils import OPERATIONS_FOR_NUMERICAL_FILTERS
from utility.constants import (
    COLUMN_NAME,
    JINJA_SELECT_HTML_FILE,
    ENTRIES,
    SELECT_OPTION,
    ACTIVE_SELECTORS,
    SHOW_ALL_ROW,
    AVAILABLE_PAGES,
    GRAPHICS,
    SELECTABLE_DATA_LIST,
)


def test_extract_buttons(json_config_fixture):
    aval_pg = json_config_fixture["available_pages"]
    buttons = create_link_buttons_for_available_pages(aval_pg)

    button1 = {"button_label": "Penguins", "link": "penguins"}
    assert button1 in buttons


def test_create_data_subselect_info(local_handler_fixture, json_config_fixture):
    select_dict = [
        {
            "type": "select",
            "column": "penguin_size:sex",
            "options": {"multiple": False},
            ACTIVE_SELECTORS: ["MALE"],
        },
        {
            "type": "select",
            "column": "penguin_size:island",
            "options": {"multiple": True},
            ACTIVE_SELECTORS: [SHOW_ALL_ROW],
        },
        {
            "type": "axis",
            "column": "x",
            "options": {
                "entries": [
                    "penguin_size:culmen_length_mm",
                    "penguin_size:flipper_length_mm",
                    "penguin_size:body_mass_g",
                ]
            },
            ACTIVE_SELECTORS: ["penguin_size:culmen_length_mm"],
        },
    ]
    json_config_fixture[SELECTABLE_DATA_LIST] = select_dict
    select_info = create_data_subselect_info_for_plot(
        json_config_fixture, local_handler_fixture
    )

    assert select_info[0][JINJA_SELECT_HTML_FILE] == "select_filter.html"
    assert select_info[1][COLUMN_NAME] == "penguin_size:island"
    assert select_info[2][JINJA_SELECT_HTML_FILE] == "select_axis.html"

    assert "MALE" in select_info[0][ACTIVE_SELECTORS]
    assert "MALE" in select_info[0][ENTRIES]
    assert "FEMALE" in select_info[0][ENTRIES]
    assert "." in select_info[0][ENTRIES]  # yes this is a unique entry in the data set
    assert SHOW_ALL_ROW in select_info[1][ACTIVE_SELECTORS]
    assert "Biscoe" in select_info[1][ENTRIES]
    assert select_info[1][SELECT_OPTION]["multiple"]
    assert not select_info[0][SELECT_OPTION]["multiple"]
    assert "penguin_size:culmen_length_mm" in select_info[2][ENTRIES]
    assert "penguin_size:flipper_length_mm" in select_info[2][ENTRIES]
    assert "penguin_size:body_mass_g" in select_info[2][ENTRIES]
    assert "penguin_size:culmen_length_mm" in select_info[2][ACTIVE_SELECTORS]


def test_get_unique_set_of_columns_needed():
    culmen = "penguin_size:culmen_length_mm"
    flipper = "penguin_size:flipper_length_mm"
    flipper2 = "penguin_size:flipper_length_mm2"
    island = "penguin_size:island"
    sex = "penguin_size:sex"
    test_cols_list = get_unique_set_of_columns_needed(
        {
            "points_0": {"x": culmen, "y": flipper},
            "points_1": {"x": culmen, "y": flipper2},
        },
        [
            {"type": "hover_data", "column": [sex, culmen]},
            {"type": "groupby", "column": [island]},
        ],
    )
    assert culmen in test_cols_list
    assert flipper in test_cols_list
    assert flipper2 in test_cols_list
    assert island in test_cols_list
    assert sex in test_cols_list
    assert len(test_cols_list) == 5


def test_get_data_selection_info_for_page_render(
    local_handler_fixture, json_config_fixture
):
    plot_specification = json_config_fixture[AVAILABLE_PAGES]["penguins"][GRAPHICS][
        "graphic_0"
    ]
    # add_active_selectors_to_selectable_data_list adds default  SHOW_ALL_ROWS to selectors
    for selector in plot_specification[SELECTABLE_DATA_LIST]:
        selector[ACTIVE_SELECTORS] = [SHOW_ALL_ROW]
    select_info = get_data_selection_info_for_page_render(
        plot_specification, local_handler_fixture
    )

    expected_select_info = [
        {
            "select_html_file": "select_filter.html",
            "type": "filter",
            "column": "penguin_size:sex",
            "active_selector": ["SHOW_ALL_ROW"],
            "entries": [".", "FEMALE", "MALE"],
            "options": {"multiple": False},
        },
        {
            "select_html_file": "select_filter.html",
            "type": "filter",
            "column": "penguin_size:island",
            "active_selector": ["SHOW_ALL_ROW"],
            "entries": ["Biscoe", "Dream", "Torgersen"],
            "options": {"multiple": True},
        },
        {
            "select_html_file": "numerical_filter.html",
            "type": "numerical_filter",
            "column": "penguin_size:culmen_length_mm",
            "active_selector": ["SHOW_ALL_ROW"],
            "entries": OPERATIONS_FOR_NUMERICAL_FILTERS.keys(),
            "options": {},
        },
    ]
    assert select_info == expected_select_info


def test_remove_redundant_filters_from_active_selectors(
    local_handler_fixture, json_config_fixture
):
    plot_specification = json_config_fixture[AVAILABLE_PAGES]["penguins"][GRAPHICS][
        "graphic_0"
    ]
    # Male should be removed from this because we're also selecting SHOW_ALL_ROW
    selectable_list_1 = plot_specification[SELECTABLE_DATA_LIST][0]
    selectable_list_1.update({ACTIVE_SELECTORS: [SHOW_ALL_ROW, "MALE"]})
    selectable_list_2 = plot_specification[SELECTABLE_DATA_LIST][1]
    selectable_list_2.update({ACTIVE_SELECTORS: ["Biscoe"]})
    remove_redundant_filters_from_active_selectors(
        plot_specification[SELECTABLE_DATA_LIST]
    )

    assert selectable_list_2[ACTIVE_SELECTORS] == ["Biscoe"]
    assert selectable_list_1[ACTIVE_SELECTORS] == [SHOW_ALL_ROW]
