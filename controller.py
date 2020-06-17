from datastorer.local_handler import LocalHandler
from graphics.available_graphics import AVAILABLE_GRAPHICS
import json


def get_data_for_page(config_file_path: str, disp_pg) -> dict:
    """
    :param config_file:
    :return:
    """
    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)
    aval_pg=config_dict["available_pages"]
    if disp_pg is not None:
        plot_list = aval_pg[disp_pg]["graphics"]
        plot_specs = organize_graphic(plot_list)
    else:
        plot_specs = []

    buttons = extract_buttons(aval_pg)

    page_info = {
        "plots": plot_specs,
        "title": config_dict["title"],
        "brief_desc": config_dict["brief_desc"],
        "buttons":buttons
    }
    return page_info


def organize_graphic(plot_list: list) -> list:
    plot_specs = []

    for plot_dict in plot_list:
        new_data = LocalHandler("tests/test_data/Penguins_size/penguins_size.csv")
        data_dict = new_data.get_column_data(plot_dict["data"])
        graphic_data = AVAILABLE_GRAPHICS[plot_dict["plot_manager"]]
        new_graphic = graphic_data["object"]
        jsonstr = new_graphic.draw(
            data_dict, plot_dict["data_to_plot_path"], plot_dict["plot_options"]
        )
        html_dict = {
            "html_file": graphic_data["graph_html_template"],
            "title": plot_dict["title"],
            "brief_desc": plot_dict["brief_desc"],
            "plot_info": jsonstr,
        }
        plot_specs.append(html_dict)
    return plot_specs


def extract_buttons(aval_pages: dict) -> list:
    buttons=[]
    for key in aval_pages.keys():
        buttons.append({'name':aval_pages[key]['name'],
                        'link':key})
    return buttons