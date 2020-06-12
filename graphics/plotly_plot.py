import json

from graphics.graphic_class import Graphic

import plotly


class PlotlyPlot(Graphic):
    def __init__(self, type):
        """

        :param type: type of plotly graph - 'bar', 'scatter'
        :returns: filename and JSON file
        """
        super().__init__()
        self.type = type

    def draw(self, data, axis_names):
        """

        :param data: The data that wil be ploted list of lists
        :param axis_names: names of the various axis
        :return:
        """
        graphinfo = dict(
            data=[dict(type=self.type, x=data[0], y=data[1], mode="markers"),],
            layout=dict(
                title="Penquin test data",  # will be changed
                xaxis=dict(title=axis_names[0]),
                yaxis=dict(title=axis_names[1]),
            ),
        )
        graphJSON = json.dumps(
            graphinfo, cls=plotly.utils.PlotlyJSONEncoder
        )  # I decided that I want to keep the strings here
        return "datalayout.html", graphJSON

    def update_graphic(self, data):
        super().update_graphic(data)

    def get_options(self):
        super().get_options()
