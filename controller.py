from datastorer.data_handler import DataHandler
from datastorer.local_handler import LocalCSVHandler
from utility.available_graphics import AVAILABLE_GRAPHICS
from utility.available_selectors import AVAILABLE_SELECTORS
from utility.constants import *


def get_data_for_page(config_dict: dict, display_page, form=None) -> dict:
    """

    :param config_dict: A dictionary containing all the information from the config json file
    :param display_page: Which page is the viewer requesting
    :param form: form request received from push request.
    :return: dictionary to be read by jinja to build the page
    """
    filter_dict = {}
    axis_dict = {}
    if form is not None:
        [filter_dict, axis_dict] = reformatting_the_form_dict(form)

    available_pages = config_dict[AVAILABLE_PAGES]
    if display_page is not None:
        plot_list = available_pages.get(display_page, {}).get(GRAPHICS, [])
        plot_specs = organize_graphic(plot_list, filter_dict, axis_dict)
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


def organize_graphic(plot_list: list, filter_dict={}, axis_dict={}) -> list:
    """
    creates dictionary to be read in by the html file to plot the graphics and selectors
    :param plot_list:
    :param filter_dict:
    :param axis_dict:
    :return:
    """
    plot_specs = []

    for index, plot_dict in enumerate(plot_list):
        new_data = LocalCSVHandler(
            plot_dict[DATA_PATH]
        )  # TO DO Need to allow for database
        filters = {}
        axis_change = {}
        if index in filter_dict:
            filters = filter_dict[index]  # finds filters for the data

        if index in axis_dict:
            axis_change = axis_dict[index]  # finds filters for the data

        axis_to_data_columns = plot_dict[DATA]
        axis_to_data_columns.update(axis_change)
        hover_data = []
        if HOVER_DATA in plot_dict:
            hover_data = plot_dict[HOVER_DATA]
        data_dict = new_data.get_column_data(
            extract_data_needed(axis_to_data_columns, hover_data),
            filters,  # retrieves all needed columns
        )
        graphic_data = AVAILABLE_GRAPHICS[
            plot_dict[PLOT_MANAGER]
        ]  # Checks to see if it is a valid graphic
        # TO DO what if it is not
        new_graphic = graphic_data[OBJECT]
        jsonstr = new_graphic.draw(
            data_dict,
            axis_to_data_columns,
            plot_dict[PLOT_OPTIONS],
            hover_data,  # makes a json file as required by js plotting documentation
        )
        if (
            SELECTABLE_DATA_LIST in plot_dict.keys()
        ):  # checks to see if this plot has selectors
            select_dict = plot_dict[SELECTABLE_DATA_LIST]
            select_info = create_select_info(
                select_dict, new_data, filters, axis_to_data_columns
            )

        else:
            select_info = []
        html_dict = {
            JINJA_GRAPH_HTML_FILE: graphic_data[GRAPH_HTML_TEMPLATE],
            JINJA_SELECT_INFO: select_info,
            GRAPHIC_TITLE: plot_dict[GRAPHIC_TITLE],
            GRAPHIC_DESC: plot_dict[GRAPHIC_DESC],
            JINJA_PLOT_INFO: jsonstr,
        }
        plot_specs.append(html_dict)
    return plot_specs


def extract_data_needed(data_list: list, hover_data: list = []) -> list:
    """
    Returns the unique columns of the data we need to get
    TO DO throw an error if contains column names not in data

    :param data_list:
    :param hover_data:
    :return:
    """
    data_set = set()
    for data_dict in data_list:
        data_set.update(data_dict.values())
    data_set.update(hover_data)
    return list(data_set)


def create_link_buttons_for_available_pages(available_pages: dict) -> list:
    """

    :param available_pages:
    :return:
    """
    buttons = []
    for key in available_pages.keys():
        buttons.append({"name": available_pages[key][PAGE_NAME], "link": key})
    return buttons


def create_select_info(
    select_list: list, new_data: DataHandler, filters: dict, axis_to_data_columns: dict
) -> list:
    """
    puts selctor data in form to be read by html file
    :param select_list:
    :param new_data:
    :param filters:
    :param axis_to_data_columns:
    :return:
    """
    select_info = []
    for select_dict in select_list:
        active = []
        selector_attributes = AVAILABLE_SELECTORS[select_dict[OPTION_TYPE]]
        select_html_file = selector_attributes[SELECT_HTML_TEMPLATE]
        column = select_dict[OPTION_COLS]
        columns_names = []
        if select_dict[SELECTOR_TYPE] == SELECTOR:
            columns_names = new_data.get_column_unique_entries([column])
            columns_names = columns_names[column]
            if column in filters:
                active = filters[column]
        elif select_dict[SELECTOR_TYPE] == AXIS:
            columns_names = select_dict[SELECT_OPTION][ENTRIES]
            if column in axis_to_data_columns:
                active = [axis_to_data_columns[column]]

        select_info.append(
            {
                JINJA_SELECT_HTML_FILE: select_html_file,
                SELECTOR_TYPE: selector_attributes[SELECTOR_TYPE],
                COLUMN_NAME: column,
                ACTIVE_SELECTORS: active,
                ENTRIES: columns_names,
                SELECT_OPTION: select_dict[SELECT_OPTION],
            }
        )

    return select_info


def reformatting_the_form_dict(form_dict: dict) -> [dict, dict]:
    """
    Because it is easier to use a nested dictionary in organize_graphic for getting the data
    then the default form request from flask
    :param form_dict:
    :return:
    """
    filter_dict = {}
    axis_dict = {}
    for key, values in form_dict.lists():
        [plot_index, selector_type, column_name] = key.split("_", 2)
        if selector_type == SELECTOR:
            if SHOW_ALL_ROW not in values:  # Made a choice about behavior
                plot_index = int(plot_index)
                if plot_index in filter_dict:
                    filter_dict[plot_index][column_name] = values
                else:
                    filter_dict[plot_index] = {column_name: values}
        elif selector_type == AXIS:
            plot_index = int(plot_index)
            if plot_index in filter_dict:
                filter_dict[plot_index][column_name] = values
            else:
                filter_dict[plot_index] = {column_name: values}

    return filter_dict, axis_dict
