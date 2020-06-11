import json

from graphics.graphic_class import Graphic

import plotly


class PlotlyPlot(Graphic):

    def __init__(self, type):
        '''

        :param type: type of plotly graph - 'bar', 'line'
        :returns: filename and JSON file
        '''
        super().__init__()
        self.type = type

    def draw(self, data):
        graphinfo = dict(
            data=[
                dict(
                    type=self.type,
                    x=data[0],
                    y=data[1]
                ),
            ],
            layout=dict(
                title='test graph')
        )
        graphJSON = json.dumps(graphinfo, cls=plotly.utils.PlotlyJSONEncoder)
        return 'plotly.html', graphJSON

    def update_graphic(self, data):
        super().update_graphic(data)

    def get_options(self):
        super().get_options()
