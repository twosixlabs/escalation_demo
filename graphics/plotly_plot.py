import json

from graphics.graphic_class import Graphic

import plotly


class PlotlyPlot(Graphic):
    def __init__(self):
        """
        :param type: type of plotly graph - 'bar', 'scatter'
        """

    def draw(self, data, data_to_struct, plot_options):
        """
        :param plot_dict: The data that wil be ploted list of lists
        :return: json
        """
        for key, path in data_to_struct.items():
            plot_options[path[0]][path[1]][path[2]] = data[key]  # three things in path

        graphJSON = json.dumps(
            plot_options, cls=plotly.utils.PlotlyJSONEncoder
        )  # I decided that I want to keep the strings here
        return graphJSON
