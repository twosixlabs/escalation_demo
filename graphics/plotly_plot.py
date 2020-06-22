import json

from graphics.graphic_class import Graphic

import plotly

DATA = "data"
LAYOUT = "layout"
AXIS = "{}axis"
TITLE = "title"


class PlotlyPlot(Graphic):
    def draw(self, data, axis_to_data_columns, plot_options, hover_data=[]):

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
            if len(hover_data) > 0:
                hover_data_list = []
                hover_template_list = []
                for hover_index, hover_col in enumerate(hover_data):
                    hover_data_list.append(data[hover_col])
                    hover_template_list.append(
                        "".join([hover_col, ": %{customdata[", str(hover_index), "]}"])
                    )
                hover_template_list.append("<extra></extra>")
                plot_options[DATA][index]["hovertemplate"] = "<br>".join(
                    hover_template_list
                )
                plot_options[DATA][index]["customdata"] = list(
                    map(list, zip(*hover_data_list))
                )  # transpose

        graph_json = json.dumps(
            plot_options, cls=plotly.utils.PlotlyJSONEncoder
        )  # I decided that I want to keep the strings here
        return graph_json
