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
VISUALIZATION_TYPE = "type"
TRANSFORMS = "transforms"
GROUPBY = "groupby"
AGGREGATE = "aggregate"
HOVER_DATA = "hover_data"
GROUPS = "groups"
OPTIONS = "options"
STYLES = "styles"
AGGREGATIONS = "aggregations"


def get_hover_data_in_plotly_form(data, hover_options, plot_options_data_dict):
    """

    :param data:
    :param hover_column_names:
    :param plot_options_data_dict:
    :param index:
    :return:
    """
    # if data is a dataframe: plot_options[DATA][index]["customdata"] = data[hover_data].values.tolist()
    # is equalavent to the two lines function
    hover_column_names = hover_options[DATA]
    hover_data_list = [data[hover_col_name] for hover_col_name in hover_column_names]
    plot_options_data_dict[CUSTOM_DATA] = list(map(list, zip(*hover_data_list)))

    plot_options_data_dict[HOVER_TEMPLATE] = render_template(
        HOVER_TEMPLATE_HTML, hover_column_names=hover_column_names
    )
    return plot_options_data_dict


def get_groupby_in_plotly_form(data, group_by, plot_options_data_dict):
    """
    if group_by has options
     We only allow the key styles
     we expect a dictionary of styles g.e. col_name: {marker: {color: blue}}
    :param data:
    :param group_by:
    :param plot_options_data_dict:
    :return:
    """
    group_by_dict = {VISUALIZATION_TYPE: GROUPBY, GROUPS: data[group_by[DATA][0]]}
    if OPTIONS in group_by:
        style_dict = group_by[OPTIONS][STYLES]
        plotly_style_list = [
            {"target": col_name, "value": style}
            for col_name, style in style_dict.items()
        ]
        group_by_dict[STYLES] = plotly_style_list

    plot_options_data_dict[TRANSFORMS].append(group_by_dict)
    return plot_options_data_dict


def get_aggregate_in_plotly_form(data, aggregate, plot_options_data_dict):
    """
    You have to have aggregations in your options column
    :param data:
    :param aggregate:
    :param plot_options_data_dict:
    :return:
    """
    aggregate_dict = {VISUALIZATION_TYPE: AGGREGATE, GROUPS: data[aggregate[DATA][0]]}

    # attribute_name can be x, y or something like marker.size
    # func can be avg, min, sum, count, stddev etc.
    attribute_dict = aggregate[OPTIONS][AGGREGATIONS]
    plotly_aggregations_list = [
        {"target": attribute_name, "func": func}
        for attribute_name, func in attribute_dict.items()
    ]
    aggregate_dict[AGGREGATIONS] = plotly_aggregations_list

    plot_options_data_dict[TRANSFORMS].append(aggregate_dict)
    return plot_options_data_dict


VISUALIZATION_OPTIONS = {
    HOVER_DATA: get_hover_data_in_plotly_form,
    GROUPBY: get_groupby_in_plotly_form,
    AGGREGATE: get_aggregate_in_plotly_form,
}


class PlotlyPlot(Graphic):
    def make_dict_for_html_plot(
        self, data, axis_to_data_columns, plot_options, visualization_options=None
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
            plot_options[DATA][index][TRANSFORMS] = []

            if visualization_options is not None:
                for extra_visualization_feature in visualization_options:
                    plot_options[DATA][index] = VISUALIZATION_OPTIONS[
                        extra_visualization_feature[VISUALIZATION_TYPE]
                    ](data, extra_visualization_feature, plot_options[DATA][index])

        graph_json = json.dumps(plot_options, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
