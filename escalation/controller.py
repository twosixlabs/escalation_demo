import copy

from flask import current_app

from database.data_handler import DataHandler
from graphics.utils.available_graphics import AVAILABLE_GRAPHICS
from graphics.utils.available_selectors import AVAILABLE_SELECTORS
from graphics.utils.reformatting_functions import add_instructions_to_config_dict
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
        plot_specs = organize_graphic(single_page_config_dict)

    page_info = {
        JINJA_PLOT: plot_specs,
        SITE_TITLE: config_dict[SITE_TITLE],
        SITE_DESC: config_dict[SITE_DESC],
    }
    return page_info


def organize_graphic(single_page_config_dict: dict) -> list:
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

        (plot_directions_dict, graph_html_template) = assemble_info_for_plot(
            plot_specification, plot_data_handler
        )

        select_info = []
        # checks to see if this plot has selectors
        if SELECTABLE_DATA_LIST in plot_specification:
            select_dict = plot_specification[SELECTABLE_DATA_LIST]
            select_info = create_data_subselect_info(select_dict, plot_data_handler)

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


def assemble_info_for_plot(plot_specification, plot_data_handler):
    """
    assembles the dictionary needed to render the graphic
    a string with the html file that use the aforementioned dictionary
    The dashboard options
    :param plot_specification:
    :param plot_data_handler:
    :return:
    """

    visualization_options = plot_specification.get(VISUALIZATION_OPTIONS, [])
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
    data_dict_to_be_plotted: dict, list_of_plot_metadata: list = None
) -> list:
    """
    Returns the unique columns of the data we need to get
    TO DO throw an error if contains column names not in data

    :param data_dict_to_be_plotted:
    :param list_of_plot_metadata:
    :return:
    """
    set_of_column_names = set()
    for dict_of_data_on_each_axis in data_dict_to_be_plotted.values():
        set_of_column_names.update(dict_of_data_on_each_axis.values())
    if list_of_plot_metadata is not None:
        set_of_column_names.update(
            {
                col_name
                for visualization in list_of_plot_metadata
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


def create_data_subselect_info(
    list_of_selection_options_by_plot: list, data_handler: DataHandler
) -> list:
    """
    puts selector data in form to be read by html file
    :param list_of_selection_options_by_plot: SELECTABLE_DATA_LIST entry in the json
    :param data_handler:
    :return:
    """
    select_info = []
    for selection_index, selection_option_dict_for_plot in enumerate(
        list_of_selection_options_by_plot
    ):

        selector_attributes = AVAILABLE_SELECTORS[
            selection_option_dict_for_plot[OPTION_TYPE]
        ]
        select_html_file = selector_attributes[SELECT_HTML_TEMPLATE]
        column = selection_option_dict_for_plot[OPTION_COL]
        column_names = []

        if selection_option_dict_for_plot[SELECTOR_TYPE] == SELECTOR:
            column_names = data_handler.get_column_unique_entries([column])
            column_names = column_names[column]
            column_names.sort()
        elif selection_option_dict_for_plot[SELECTOR_TYPE] == AXIS:
            column_names = selection_option_dict_for_plot[SELECT_OPTION][ENTRIES]
            column_names.sort()
        elif selection_option_dict_for_plot[SELECTOR_TYPE] == NUMERICAL_FILTER:
            column_names = OPERATIONS_FOR_NUMERICAL_FILTERS.keys()

        active_selection_options = selection_option_dict_for_plot[ACTIVE_SELECTORS]

        select_info.append(
            {
                JINJA_SELECT_HTML_FILE: select_html_file,
                SELECTOR_TYPE: selector_attributes[SELECTOR_TYPE],
                COLUMN_NAME: column,
                ACTIVE_SELECTORS: active_selection_options,
                ENTRIES: column_names,
                SELECT_OPTION: selection_option_dict_for_plot.get(SELECT_OPTION, {}),
            }
        )

    return select_info
