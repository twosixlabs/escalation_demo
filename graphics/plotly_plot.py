import json
import plotly
from flask import render_template
from graphics.graphic_class import Graphic

HOVER_TEMPLATE_HTML = "hover_template.html"

DATA = "data"
LAYOUT = "layout"
AXIS = "{}axis"
TITLE = "title"
CUSTOM_DATA = "customdata"
HOVER_TEMPLATE = "hovertemplate"


def get_hover_data_in_plotly_form(data, hover_column_names):
    """
    if data is a dataframe:
    plot_options[DATA][index]["customdata"] = data[hover_data].values.tolist()
    is equalavent to this function

    :param data:
    :param hover_column_names:
    :return:
    """

    hover_data_list = []
    for hover_col_name in hover_column_names:
        hover_data_list.append(data[hover_col_name])

    return list(map(list, zip(*hover_data_list)))  # transpose list of lists


class PlotlyPlot(Graphic):
    def make_dict_for_html_plot(
        self, data, axis_to_data_columns, plot_options, hover_column_names=None
    ):

        for index, axis_to_data_dict in enumerate(axis_to_data_columns):
            for axis, column_name in axis_to_data_dict.items():
                plot_options[DATA][index][axis] = data[
                    column_name
                ]  # three things in path, data, which index and value (x,y)
                if index == 0:
                    if LAYOUT in plot_options:
                        plot_options[LAYOUT][AXIS.format(axis)] = {TITLE: column_name}
                    else:
                        plot_options[LAYOUT] = {AXIS.format(axis): {TITLE: column_name}}

            if hover_column_names is None:
                continue
            plot_options[DATA][index][CUSTOM_DATA] = get_hover_data_in_plotly_form(
                data, hover_column_names
            )
            plot_options[DATA][index][HOVER_TEMPLATE] = render_template(
                HOVER_TEMPLATE_HTML, hover_column_names=hover_column_names
            )

        graph_json = json.dumps(plot_options, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
