import json

from graphics.graphic_class import Graphic

import plotly


class PlotlyPlot(Graphic):
    def draw(self, data, data_to_plot_path, plot_options):
        """

        :param data:
        :param data_to_plot_path:
        :param plot_options:
        :return:
        """
        for key, path in data_to_plot_path.items():
            plot_options[path[0]][path[1]][path[2]] = data[
                key
            ]  # three things in path, data, which index and value (x,y)

        graph_json = json.dumps(
            plot_options, cls=plotly.utils.PlotlyJSONEncoder
        )  # I decided that I want to keep the strings here
        return graph_json
