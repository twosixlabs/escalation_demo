from datastorer.data_handler import DataHandler
from datastorer.local_handler import LocalCSVHandler
from utility.available_graphics import AVAILABLE_GRAPHICS
from utility.available_selectors import AVAILABLE_SELECTORS
from utility.constants import *


def get_data_for_page(config_dict: dict, display_pages) -> dict:
    """
    :param config_dict:
    :param display_pages:
    :return:
    """

    available_pages = config_dict[AVAILABLE_PAGES]
    if display_pages is not None:
        plot_list = available_pages[display_pages][GRAPHICS]
        plot_specs = organize_graphic(plot_list)
    else:
        plot_specs = []

    buttons = create_link_buttons_for_available_pages(available_pages)

    page_info = {
        "plots": plot_specs,
        "title": config_dict[SITE_TITLE],
        "brief_desc": config_dict[SITE_DESC],
        "buttons": buttons,
    }
    return page_info


def organize_graphic(plot_list: list) -> list:
    plot_specs = []

    for plot_dict in plot_list:
        new_data = LocalCSVHandler(plot_dict[DATA_PATH])
        data_dict = new_data.get_column_data(plot_dict[DATA])
        graphic_data = AVAILABLE_GRAPHICS[plot_dict[PLOT_MANAGER]]
        new_graphic = graphic_data[OBJECT]
        jsonstr = new_graphic.draw(
            data_dict, plot_dict[DATA_TO_PLOT_PATH], plot_dict[PLOT_OPTIONS]
        )
        if OPTION_BAR in plot_dict.keys():
            select_dict = plot_dict[OPTION_BAR]
            [select_html_file, select_info] = create_select_info(select_dict, new_data)

        else:
            select_html_file = ""
            select_info = {}
        html_dict = {
            "graph_html_file": graphic_data[
                GRAPH_HTML_TEMPLATE
            ],  # make these string constants
            "select_html_file": select_html_file,
            "select_info": select_info,
            "title": plot_dict[GRAPHIC_TITLE],
            "brief_desc": plot_dict[GRAPHIC_DESC],
            "plot_info": jsonstr,
        }
        plot_specs.append(html_dict)
    return plot_specs


def create_link_buttons_for_available_pages(available_pages: dict) -> list:
    buttons = []
    for key in available_pages.keys():
        buttons.append({"name": available_pages[key][PAGE_NAME], "link": key})
    return buttons


def create_select_info(select_dict: dict, new_data: DataHandler) -> [str, dict]:

    selector_attributes = AVAILABLE_SELECTORS[select_dict[OPTION_TYPE]]
    select_html_file = selector_attributes[SELECT_HTML_TEMPLATE]
    columns = select_dict[OPTION_COLS]
    select_info = new_data.get_column_unique_entries(columns)

    return select_html_file, select_info
