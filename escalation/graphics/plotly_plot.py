# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import json
import plotly
from flask import render_template
from graphics.graphic_class import Graphic
from utility.constants import OPTION_COL, GROUPBY, AGGREGATE, HOVER_DATA, AGGREGATIONS

HOVER_TEMPLATE_HTML = "hover_template.html"

DATA = "data"
LAYOUT = "layout"
PLOT_AXIS = "{}axis"
TITLE = "title"
CUSTOM_DATA = "customdata"
HOVER_TEMPLATE = "hovertemplate"
VISUALIZATION_TYPE = "type"
PLOTLY_TYPE = "type"
TRANSFORMS = "transforms"
GROUPS = "groups"
OPTIONS = "options"
STYLES = "styles"
PLOT_OPTIONS = "plot_options"
NA_FILL_IN = "NA"
TABLE = "table"
CELLS = "cells"
HEADER = "header"
VALUES = "values"
MODE = "mode"
LINES = "lines"
AXIS_TO_SORT_ALONG = "x"
AUTOMARGIN = "automargin"
HOVERMODE = "hovermode"
CLOSEST = "closest"


def get_hover_data_in_plotly_form(
    data, hover_options, visualization_type, plot_options_data_dict
):
    """

    :param data:
    :param hover_options:
    :param plot_options_data_dict:
    :return:
    """
    # if data is a dataframe: plot_options[DATA][index]["customdata"] = data[hover_data].values.tolist()
    # is equivalent to the two lines function
    hover_column_names = hover_options[OPTION_COL]
    # hover_data_list = [data[hover_col_name] for hover_col_name in hover_column_names]
    # transposes a list of lists of column data to a list of lists of row data
    plot_options_data_dict[CUSTOM_DATA] = (
        data[hover_column_names].astype(str).values.tolist()
    )

    plot_options_data_dict[HOVER_TEMPLATE] = render_template(
        HOVER_TEMPLATE_HTML, hover_column_names=hover_column_names
    )
    return plot_options_data_dict


def get_groupby_or_aggregate_in_plotly_form(
    data, visualization_property, visualization_type, plot_options_data_dict
):
    """
    aggregate allows you to do a function on an aggregation of the data
    group_by allows you to change the color based on one of the columns
    if group_by has options we only allow the key styles
     we expect a dictionary of styles g.e. col_name: {marker: {color: blue}}
    :param data:
    :param visualization_property: a dictionary that includes the type (groupby or aggregate), column name (stored in a list of length one)
    and options such as color for groupby and function for aggregate
    :param plot_options_data_dict:
    :return:
    """
    group_labels = [
        ", ".join(data_list)
        for data_list in data[visualization_property[OPTION_COL]]
        .astype(str)
        .values.tolist()
    ]
    property_dict = {
        VISUALIZATION_TYPE: visualization_type,
        GROUPS: group_labels,
    }

    if visualization_type == GROUPBY and STYLES in visualization_property:
        style_dict = visualization_property[STYLES]
        plotly_style_list = [
            {"target": col_name, "value": style}
            for col_name, style in style_dict.items()
        ]
        property_dict[STYLES] = plotly_style_list
    elif visualization_type == AGGREGATE:
        # attribute_name can be x, y or something like marker.size
        # func can be avg, min, sum, count, stddev etc.
        attribute_dict = visualization_property[AGGREGATIONS]
        plotly_aggregations_list = [
            {"target": attribute_name, "func": func}
            for attribute_name, func in attribute_dict.items()
        ]
        property_dict[AGGREGATIONS] = plotly_aggregations_list

    plot_options_data_dict[TRANSFORMS].append(property_dict)
    return plot_options_data_dict


VISUALIZATION_OPTIONS = {
    HOVER_DATA: get_hover_data_in_plotly_form,
    GROUPBY: get_groupby_or_aggregate_in_plotly_form,
    AGGREGATE: get_groupby_or_aggregate_in_plotly_form,
}


def does_data_need_to_be_sorted(plot_info_data_dict: dict):
    """
    Determines whether the data needs to be sorted if so does it inplace
    :param data_dict:
    :return:
    """
    # conditions when data needs to be sorted
    if plot_info_data_dict[PLOTLY_TYPE] == "scatter" and (
        MODE not in plot_info_data_dict or LINES in plot_info_data_dict[MODE]
    ):
        return True
    return False


def add_layout_axis_defaults(layout_dict: dict, axis, column_name):
    """
    Adds defaults to the layout to the plotly graph for a better viewing experience
    :param layout_dict:
    :param axis:
    :param column_name:
    :return:
    """
    if PLOT_AXIS.format(axis) not in layout_dict:
        layout_dict[PLOT_AXIS.format(axis)] = {TITLE: column_name}
    if AUTOMARGIN not in layout_dict[PLOT_AXIS.format(axis)]:
        layout_dict[PLOT_AXIS.format(axis)][AUTOMARGIN] = True
    return layout_dict


class PlotlyPlot(Graphic):
    def make_dict_for_html_plot(
        self, data, axis_to_data_columns, plot_options, visualization_options=None
    ):
        """
        Makes the json file that plotly takes in
        :param data: a pandas dataframe
        :param axis_to_data_columns:
        :param plot_options:
        :param visualization_options:
        :return:
        """
        # todo: cut off all text data to used in group by or titles to 47 charaters
        data_sorted = False
        for index, axis_to_data_dict in enumerate(axis_to_data_columns):
            if plot_options[DATA][index][PLOTLY_TYPE] == TABLE:
                values = []
                header = []
                # adding the data and headers into the table
                for axis, column_name in axis_to_data_dict.items():
                    values.append(data[column_name])
                    header.append(axis)
                for table_key, values_for_dict in zip(
                    [CELLS, HEADER], [values, header]
                ):
                    temp_dict = plot_options[DATA][index].get(table_key, {})
                    temp_dict[VALUES] = values_for_dict
                    plot_options[DATA][index][table_key] = temp_dict
            else:
                if not data_sorted and does_data_need_to_be_sorted(
                    plot_options[DATA][index]
                ):
                    data.sort_values(
                        axis_to_data_dict[AXIS_TO_SORT_ALONG], inplace=True
                    )
                    data_sorted = True
                for axis, column_name in axis_to_data_dict.items():
                    # three things in path, data, which index and value (x,y)
                    plot_options[DATA][index][axis] = data[column_name]
                    # if there is no label, label the columns with the first lines/scatters column names
                    if index == 0:
                        layout_dict = plot_options.get(LAYOUT, {})
                        if HOVERMODE not in layout_dict:
                            layout_dict[HOVERMODE] = CLOSEST
                        plot_options[LAYOUT] = add_layout_axis_defaults(
                            layout_dict, axis, column_name
                        )

            plot_options[DATA][index][TRANSFORMS] = []

            if visualization_options is not None:
                for (
                    visualization_type,
                    visualization_parameters,
                ) in visualization_options.items():
                    plot_options[DATA][index] = VISUALIZATION_OPTIONS[
                        visualization_type
                    ](
                        data,
                        visualization_parameters,
                        visualization_type,
                        plot_options[DATA][index],
                    )

        graph_json = json.dumps(plot_options, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
