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
        JINJA_PLOT: plot_specs,  # jinja
        SITE_TITLE: config_dict[SITE_TITLE],
        SITE_DESC: config_dict[SITE_DESC],
        JINJA_BUTTONS: buttons,
    }
    return page_info


def organize_graphic(plot_list: list, form_dict={}) -> list:
    plot_specs = []

    for index, plot_dict in enumerate(plot_list):
        new_data = LocalCSVHandler(plot_dict[DATA_PATH])
        filters = {}
        if index in form_dict:
            filters = form_dict[index]
        data_dict = new_data.get_column_data(plot_dict[DATA], filters)
        graphic_data = AVAILABLE_GRAPHICS[plot_dict[PLOT_MANAGER]]
        new_graphic = graphic_data[OBJECT]
        jsonstr = new_graphic.draw(
            data_dict, plot_dict[DATA_TO_PLOT_PATH], plot_dict[PLOT_OPTIONS]
        )
        if SELECTABLE_DATA_DICT in plot_dict.keys():
            select_dict = plot_dict[SELECTABLE_DATA_DICT]
            [select_html_file, select_info] = create_select_info(select_dict, new_data)

        else:
            select_html_file = ""
            select_info = {}
        html_dict = {
            JINJA_GRAPH_HTML_FILE: graphic_data[GRAPH_HTML_TEMPLATE],
            ACTIVE_SELECTORS: filters,
            JINJA_SELECT_HTML_FILE: select_html_file,
            JINJA_SELECT_INFO: select_info,
            GRAPHIC_TITLE: plot_dict[GRAPHIC_TITLE],
            GRAPHIC_DESC: plot_dict[GRAPHIC_DESC],
            JINJA_PLOT_INFO: jsonstr,
        }
        plot_specs.append(html_dict)
    return plot_specs


def create_link_buttons_for_available_pages(available_pages: dict) -> list:
    """

    :param available_pages:
    :return:
    """
    buttons = []
    for key in available_pages.keys():
        buttons.append({"name": available_pages[key][PAGE_NAME], "link": key})
    return buttons


def create_select_info(select_dict: dict, new_data: DataHandler) -> [str, dict]:
    """

    :param select_dict:
    :param new_data:
    :return:
    """
    selector_attributes = AVAILABLE_SELECTORS[select_dict[OPTION_TYPE]]
    select_html_file = selector_attributes[SELECT_HTML_TEMPLATE]
    columns = select_dict[OPTION_COLS]
    select_info = new_data.get_column_unique_entries(columns)

    return select_html_file, select_info


def reformatting_the_form_dict(form_dict: dict) -> dict:
    """
    Because it is easier to use a nested dictionary in organize_graphic for getting the data
    then the default form request from flask
    :param form_dict:
    :return:
    """
    new_form_dict = {}
    for key, value in form_dict.items():
        if value != SHOW_ALL_ROW:
            [plot_index, column_name] = key.split("_", 1)
            plot_index = int(plot_index)
            if plot_index in new_form_dict:
                new_form_dict[plot_index][column_name] = value
            else:
                new_form_dict[plot_index] = {column_name: value}

    return new_form_dict
