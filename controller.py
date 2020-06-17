from datastorer.local_handler import LocalHandler
from graphics.available_graphics import AVAILABLE_GRAPHICS
import json


def get_graphic(config_file_path: str) -> list:
    """
    :param config_file:
    :return:
    """
    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)
    plot_list = config_dict["graphics"]
    plot_specs = []
    for plot_dict in plot_list:
        new_data = LocalHandler("tests/test_data/penguins_size.csv")
        data_dict = new_data.get_column_data(plot_dict["data"])
        graphic_data = AVAILABLE_GRAPHICS[plot_dict["plot_name"]]
        new_graphic = graphic_data["object"]
        jsonstr = new_graphic.draw(
            data_dict, plot_dict["data_to_struct"], plot_dict["plot_options"]
        )
        html_dict = {
            "html_file": graphic_data["html"],
            "title": plot_dict["title"],
            "brief_desc": plot_dict["brief_desc"],
            "plot_info": jsonstr,
        }
        plot_specs.append(html_dict)

    return plot_specs
