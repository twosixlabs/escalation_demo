from collections import defaultdict

from flask import current_app

from datastorer.data_handler import DataHandler
from utility.available_graphics import AVAILABLE_GRAPHICS
from utility.available_selectors import AVAILABLE_SELECTORS
from utility.constants import *


def get_data_for_page(config_dict: dict, display_page, filter_form=None) -> dict:
    """

    :param config_dict: A dictionary containing all the information from the config json file
    :param display_page: Which page is the viewer requesting
    :param filter_form: form request received from push request. # todo: describe how this form is structured, and how we restructure it in reformat_html_form_dict
    :return: dictionary to be read by jinja to build the page
    """
    filter_form_dict = None
    if filter_form is not None:
        filter_form_dict = reformat_filter_form_dict(filter_form)

    available_pages = config_dict[AVAILABLE_PAGES]
    if display_page is not None:
        plot_list = available_pages.get(display_page, {}).get(GRAPHICS, [])
        plot_specs = organize_graphic(plot_list, filter_form_dict)
    else:
        plot_specs = []

    buttons = create_link_buttons_for_available_pages(available_pages)

    page_info = {
        JINJA_PLOT: plot_specs,
        SITE_TITLE: config_dict[SITE_TITLE],
        SITE_DESC: config_dict[SITE_DESC],
        JINJA_BUTTONS: buttons,
    }
    return page_info


def organize_graphic(plot_list: list, form_dict: dict = None) -> list:
    """
      creates dictionary to be read in by the html file to plot the graphics and selectors
      :param plot_list:
      :param form_dict:
      :return:
      """
    plot_specs = []
    if form_dict is None:
        form_dict = {}
    for index, plot_specification in enumerate(plot_list):
        plot_data_handler = current_app.config.data_handler(
            plot_specification[DATA_SOURCE]
        )  # TO DO Need to allow for database
        filters = {}
        if index in form_dict:
            filters = form_dict[index]  # finds filters for the data
        axis_to_data_columns = plot_specification[DATA]
        hover_data = []
        if HOVER_DATA in plot_specification:
            hover_data = plot_specification[HOVER_DATA]
        plot_data = plot_data_handler.get_column_data(
            get_unique_set_of_columns_needed(axis_to_data_columns, hover_data), filters,
        )
        graphic_data = AVAILABLE_GRAPHICS[
            plot_specification[PLOT_MANAGER]
        ]  # Checks to see if it is a valid graphic
        # TO DO what if it is not
        new_graphic = graphic_data[OBJECT]
        jsonstr = new_graphic.draw(
            plot_data,
            axis_to_data_columns,
            plot_specification[PLOT_OPTIONS],
            hover_data,  # makes a json file as required by js plotting documentation
        )
        if (
            SELECTABLE_DATA_LIST in plot_specification.keys()
        ):  # checks to see if this plot has selectors
            select_dict = plot_specification[SELECTABLE_DATA_LIST]
            select_info = create_data_subselect_info(select_dict, plot_data_handler)

        else:
            select_info = []
        html_dict = {
            JINJA_GRAPH_HTML_FILE: graphic_data[GRAPH_HTML_TEMPLATE],
            ACTIVE_SELECTORS: filters,
            JINJA_SELECT_INFO: select_info,
            GRAPHIC_TITLE: plot_specification[GRAPHIC_TITLE],
            GRAPHIC_DESC: plot_specification[GRAPHIC_DESC],
            JINJA_PLOT_INFO: jsonstr,
        }
        plot_specs.append(html_dict)
    return plot_specs


def get_unique_set_of_columns_needed(
    list_data_dict_to_be_plotted: list, list_of_data_in_hover_text: list = None
) -> list:
    """
    Returns the unique columns of the data we need to get
    TO DO throw an error if contains column names not in data

    :param list_data_dict_to_be_plotted:
    :param list_of_data_in_hover_text:
    :return:
    """
    if list_of_data_in_hover_text is None:
        list_of_data_in_hover_text = []
    set_of_column_names = set()
    for dict_of_data_on_each_axis in list_data_dict_to_be_plotted:
        set_of_column_names.update(dict_of_data_on_each_axis.values())
    set_of_column_names.update(list_of_data_in_hover_text)
    return list(set_of_column_names)


def create_link_buttons_for_available_pages(available_pages: dict) -> list:
    """

    :param available_pages:
    :return:
    """
    buttons = []
    for key in available_pages.keys():
        buttons.append({"name": available_pages[key][PAGE_NAME], "link": key})
    return buttons


def create_data_subselect_info(
    list_of_selection_options_by_plot: list, new_data: DataHandler
) -> list:
    """
    puts selctor data in form to be read by html file
    :param list_of_selection_options_by_plot:
    :param new_data:
    :return:
    """
    select_info = []
    for selection_option_dict_for_plot in list_of_selection_options_by_plot:
        selector_attributes = AVAILABLE_SELECTORS[
            selection_option_dict_for_plot[OPTION_TYPE]
        ]
        select_html_file = selector_attributes[SELECT_HTML_TEMPLATE]
        column = selection_option_dict_for_plot[OPTION_COLS]
        columns_names = new_data.get_column_unique_entries([column])
        select_info.append(
            {
                JINJA_SELECT_HTML_FILE: select_html_file,
                COLUMN_NAME: column,
                UNIQUE_ENTRIES: columns_names[column],
                SELECT_OPTION: selection_option_dict_for_plot[SELECT_OPTION],
            }
        )

    return select_info


def reformat_filter_form_dict(form_dict: dict) -> dict:
    """
    Restructure the POST form submitted by a dashboard page containing graph filtering info.
    We do this because it is easier to use a nested dictionary in organize_graphic for getting the data
    than the default form request from flask
    :param form_dict:
    :return: dict keyed by plot index and valued with a filter
    """
    new_form_dict = defaultdict(dict)
    for selector_html_id, value_chosen_in_selector in form_dict.lists():
        if SHOW_ALL_ROW in value_chosen_in_selector:
            # this plot has no filters applied
            continue
        [plot_index, column_name] = selector_html_id.split("_", 1)
        plot_index = int(plot_index)
        new_form_dict[plot_index][column_name] = value_chosen_in_selector
    return new_form_dict
