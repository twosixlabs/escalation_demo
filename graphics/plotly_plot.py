import json

from graphics.graphic_class import Graphic

import plotly

DATA = "data"
LAYOUT = "layout"
AXIS = "{}axis"
TITLE = "title"


class PlotlyPlot(Graphic):
    def draw(self, data, axis_to_data_columns, plot_options):
        """

        :param data:
        :param axis_to_data_columns:
        :param plot_options:
        :return:
        """

        for index, axis_to_data_dict in enumerate(axis_to_data_columns):
            for key, value in axis_to_data_dict.items():
                plot_options[DATA][index][key] = data[
                    value
                ]  # three things in path, data, which index and value (x,y)
                if index == 0:
                    if LAYOUT in plot_options:
                        plot_options[LAYOUT][AXIS.format(key)] = {TITLE: value}
                    else:
                        plot_options[LAYOUT] = {AXIS.format(key): {TITLE: value}}

        graph_json = json.dumps(
            plot_options, cls=plotly.utils.PlotlyJSONEncoder
        )  # I decided that I want to keep the strings here
        return graph_json
