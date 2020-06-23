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
    form_dict = {}
    if form is not None:
        form_dict = reformatting_the_form_dict(form)

    available_pages = config_dict[AVAILABLE_PAGES]
    if display_page is not None:
        plot_list = available_pages.get(display_page, {}).get(GRAPHICS, [])
        plot_specs = organize_graphic(plot_list, form_dict)
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


def organize_graphic(plot_list: list, form_dict={}) -> list:
    """
    creates dictionary to be read in by the html file to plot the graphics and selectors
    :param plot_list:
    :param form_dict:
    :return:
    """
    plot_specs = []

    for index, plot_dict in enumerate(plot_list):
        new_data = LocalCSVHandler(
            plot_dict[DATA_PATH]
        )  # TO DO Need to allow for database
        filters = {}
        if index in form_dict:
            filters = form_dict[index]  # finds filters for the data
        axis_to_data_columns = plot_dict[DATA]
        hover_data = []
        if HOVER_DATA in plot_dict:
            hover_data = plot_dict[HOVER_DATA]
        data_dict = new_data.get_column_data(
            get_unique_set_of_columns_needed(axis_to_data_columns, hover_data),
            filters,
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
            select_info = create_select_info(select_dict, new_data)

        else:
            select_info = []
        html_dict = {
            JINJA_GRAPH_HTML_FILE: graphic_data[GRAPH_HTML_TEMPLATE],
            ACTIVE_SELECTORS: filters,
            JINJA_SELECT_INFO: select_info,
            GRAPHIC_TITLE: plot_dict[GRAPHIC_TITLE],
            GRAPHIC_DESC: plot_dict[GRAPHIC_DESC],
            JINJA_PLOT_INFO: jsonstr,
        }
        plot_specs.append(html_dict)
    return plot_specs


def get_unique_set_of_columns_needed(list_data_dict_to_be_plotted: list, list_of_data_in_hover_text: list = []) -> list:
    """
    Returns the unique columns of the data we need to get
    TO DO throw an error if contains column names not in data

    :param list_data_dict_to_be_plotted:
    :param list_of_data_in_hover_text:
    :return:
    """
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


def create_select_info(list_of_selection_options_by_plot: list, new_data: DataHandler) -> list:
    """
    puts selctor data in form to be read by html file
    :param list_of_selection_options_by_plot:
    :param new_data:
    :return:
    """
    select_info = []
    for selection_option_dict_for_plot in list_of_selection_options_by_plot:
        selector_attributes = AVAILABLE_SELECTORS[selection_option_dict_for_plot[OPTION_TYPE]]
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


def reformatting_the_form_dict(form_dict: dict) -> dict:
    """
    Because it is easier to use a nested dictionary in organize_graphic for getting the data
    then the default form request from flask
    :param form_dict:
    :return:
    """
    new_form_dict = {}
    for selector_html_id, value_chosen_in_selector in form_dict.lists():
        if SHOW_ALL_ROW not in value_chosen_in_selector:  # Made a choice about behavior
            [plot_index, column_name] = selector_html_id.split("_", 1)
            plot_index = int(plot_index)
            if plot_index in new_form_dict:
                new_form_dict[plot_index][column_name] = value_chosen_in_selector
            else:
                new_form_dict[plot_index] = {column_name: value_chosen_in_selector}

    return new_form_dict
