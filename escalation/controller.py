# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import copy

from flask import current_app

from database.data_handler import DataHandler
from graphics.utils.available_graphics import AVAILABLE_GRAPHICS
from utility.available_selectors import AVAILABLE_SELECTORS
from utility.reformatting_functions import add_instructions_to_config_dict
from database.utils import OPERATIONS_FOR_NUMERICAL_FILTERS
from utility.constants import *


def get_data_for_page(config_dict: dict, display_page, addendum_dict=None) -> dict:
    """

    :param config_dict: A dictionary containing all the information from the config json file
    :param display_page: Which page is the viewer requesting
    :param addendum_dict: json received from post. # todo: describe how this form is structured, and how we restructure it in reformat_html_form_dict
    :return: dictionary to be read by jinja to build the page
    """

    available_pages = config_dict[AVAILABLE_PAGES]
    plot_specs = []
    if display_page is not None:
        single_page_config_dict = copy.deepcopy(
            available_pages.get(display_page, {}).get(GRAPHICS, {})
        )
        single_page_config_dict = add_instructions_to_config_dict(
            single_page_config_dict, addendum_dict
        )
        plot_specs = assemble_html_with_graphs_from_page_config(single_page_config_dict)

    page_info = {
        JINJA_PLOT: plot_specs,
        SITE_TITLE: config_dict[SITE_TITLE],
        SITE_DESC: config_dict[SITE_DESC],
        CURRENT_PAGE: display_page,
    }
    return page_info


def get_data_selection_info_for_page_render(plot_specification, plot_data_handler):
    select_info = []
    # checks to see if this plot has selectors
    if SELECTABLE_DATA_DICT in plot_specification:
        select_info = create_data_subselect_info_for_plot(
            plot_specification, plot_data_handler
        )
    return select_info


def assemble_html_with_graphs_from_page_config(single_page_config_dict: dict) -> list:
    """
    creates dictionary to be read in by the html file to plot the graphics and selectors
    :param plot_list:
    :param filter_dict:
    :param axes_to_show_per_plot: keyed by html_id of plot, value is dict with some of xyz keys and valued by column name
    :return:
    """
    plot_specs = []

    for plot_key, plot_specification in single_page_config_dict.items():
        plot_data_handler = current_app.config.data_handler(
            plot_specification[DATA_SOURCES]
        )

        (plot_directions_dict, graph_html_template) = assemble_plot_from_instructions(
            plot_specification, plot_data_handler
        )

        select_info = []
        # checks to see if this plot has selectors
        if SELECTABLE_DATA_DICT in plot_specification:
            select_info = get_data_selection_info_for_page_render(
                plot_specification, plot_data_handler
            )

        html_dict = {
            JINJA_GRAPH_HTML_FILE: graph_html_template,
            JINJA_SELECT_INFO: select_info,
            GRAPHIC_TITLE: plot_specification[GRAPHIC_TITLE],
            GRAPHIC_DESC: plot_specification[GRAPHIC_DESC],
            JINJA_PLOT_INFO: plot_directions_dict,
            PLOT_ID: plot_key,
        }
        plot_specs.append(html_dict)
    return plot_specs


def assemble_plot_from_instructions(plot_specification, plot_data_handler):
    """
    assembles the dictionary needed to render the graphic
    a string with the html file that use the aforementioned dictionary
    The dashboard options
    :param plot_specification:
    :param plot_data_handler:
    :return:
    """

    visualization_options = plot_specification.get(VISUALIZATION_OPTIONS, {})
    data_filters = []
    if DATA_FILTERS in plot_specification:
        data_filters = plot_specification[DATA_FILTERS]
    plot_data = plot_data_handler.get_column_data(
        get_unique_set_of_columns_needed(
            plot_specification[DATA], visualization_options
        ),
        data_filters,
    )

    # Checks to see if it is a valid graphic
    # TO DO what if it is not a valid graphic
    graphic_data = AVAILABLE_GRAPHICS[plot_specification[PLOT_MANAGER]]
    graphic_to_plot = graphic_data[OBJECT]
    # makes a json file as required by js plotting documentation
    plot_directions_dict = graphic_to_plot.make_dict_for_html_plot(
        plot_data,
        plot_specification[DATA],
        plot_specification[PLOT_SPECIFIC_INFO],
        visualization_options,
    )

    return plot_directions_dict, graphic_data[GRAPH_HTML_TEMPLATE]


def get_unique_set_of_columns_needed(
    data_list_to_be_plotted: list, dict_of_plot_metadata: dict = None
) -> list:
    """
    Returns the unique columns of the data we need to get
    TO DO throw an error if contains column names not in data

    :param data_dict_to_be_plotted:
    :param list_of_plot_metadata:
    :return:
    """
    set_of_column_names = set()
    for dict_of_data_on_each_axis in data_list_to_be_plotted:
        set_of_column_names.update(dict_of_data_on_each_axis.values())
    if dict_of_plot_metadata is not None:
        set_of_column_names.update(
            {
                col_name
                for visualization in dict_of_plot_metadata.values()
                for col_name in visualization[OPTION_COL]
            }
        )
    return list(set_of_column_names)


def create_link_buttons_for_available_pages(available_pages_dict: dict) -> list:
    """
    :param available_pages_dict:
    :return:
    """
    buttons = []
    for available_page in available_pages_dict.keys():
        buttons.append(
            {
                BUTTON_LABEL: available_pages_dict[available_page][BUTTON_LABEL],
                LINK: available_page,
            }
        )
    return buttons


def create_data_subselect_info_for_plot(
    plot_specification, data_handler: DataHandler,
) -> list:
    """
    puts selector data in form to be read by html file
    Broken into two major parts read in info from selection_option_dict_for_plot and then populate
     select_info elements
    :param plot_specification:
    :param data_handler:
    :return:
    """

    select_info = []
    selectable_data_dict = plot_specification[SELECTABLE_DATA_DICT]

    axis_list = selectable_data_dict.get(AXIS, [])
    for index, axis_dict in enumerate(axis_list):
        selector_entries = axis_dict[ENTRIES]
        selector_entries.sort()
        select_info.append(make_filter_dict(AXIS, axis_dict, index, selector_entries))

    if GROUPBY in selectable_data_dict:
        group_by_dict = selectable_data_dict[GROUPBY]
        selector_entries = group_by_dict[ENTRIES]
        selector_entries.sort()
        # append no_group_by to the front of the list
        selector_entries.insert(0, NO_GROUP_BY)
        select_info.append(
            make_filter_dict(GROUPBY, group_by_dict, "", selector_entries)
        )

    filter_list = selectable_data_dict.get(FILTER, [])
    for index, filter_dict in enumerate(filter_list):
        column = filter_dict[OPTION_COL]
        selector_entries = data_handler.get_column_unique_entries(
            [column], filters=plot_specification.get(DATA_FILTERS)
        )
        selector_entries = selector_entries[column]
        selector_entries.sort()
        # append show_all_rows to the front of the list
        selector_entries.insert(0, SHOW_ALL_ROW)
        select_info.append(
            make_filter_dict(FILTER, filter_dict, index, selector_entries)
        )

    numerical_filter_list = selectable_data_dict.get(NUMERICAL_FILTER, [])
    for index, numerical_filter_dict in enumerate(numerical_filter_list):
        selector_entries = OPERATIONS_FOR_NUMERICAL_FILTERS.keys()
        select_info.append(
            make_filter_dict(
                NUMERICAL_FILTER, numerical_filter_dict, index, selector_entries
            )
        )

    return select_info


def make_filter_dict(selector_type, select_dict, index, selector_entries):
    html_filter_dict = {SELECTOR_TYPE: selector_type}
    selector_attributes = AVAILABLE_SELECTORS[selector_type]
    column = select_dict.get(OPTION_COL, "")
    html_filter_dict[JINJA_SELECT_HTML_FILE] = selector_attributes[SELECT_HTML_TEMPLATE]
    html_filter_dict[SELECTOR_NAME] = selector_attributes[SELECTOR_NAME].format(index)
    html_filter_dict[TEXT] = selector_attributes[TEXT].format(column)
    html_filter_dict[ACTIVE_SELECTORS] = select_dict[ACTIVE_SELECTORS]
    html_filter_dict[MULTIPLE] = select_dict.get(MULTIPLE, False)
    html_filter_dict[ENTRIES] = selector_entries
    return html_filter_dict
    select_info.append(html_filter_dict)
