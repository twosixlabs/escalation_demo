# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import json
import plotly
from flask import render_template
from graphics.graphic_class import Graphic
from utility.constants import COLUMN_NAME, DATA, LAYOUT, OPTIONS

HEADER_INFO = "header_info"


class BootstrapTable(Graphic):
    def make_dict_for_html_plot(self, data, plot_options, visualization_options=None):
        """
        Makes the dictionary that bootstrap_table.html takes in.
        layout options for bootstrap_table are currently not implemented.
        based on https://bootstrap-table.com/
        :param data: a pandas dataframe
        :param plot_options:
        :param visualization_options: not used
        :return:
        """
        list_of_column_names = self.remove_duplicate_column_names(plot_options[DATA])
        table_dict = {
            HEADER_INFO: plot_options[DATA],
            DATA: json.dumps(data[list_of_column_names].to_dict("records")),
            OPTIONS: plot_options.get(OPTIONS, {}),
        }
        return table_dict

    def get_data_columns(self, plot_options) -> set:
        """
        extracts what columns of data are needed from the plot_options
        :param plot_options:
        :return:
        """
        set_of_column_names = set()
        for dict_of_data_for_each_column in plot_options[DATA]:
            set_of_column_names.add(dict_of_data_for_each_column[COLUMN_NAME])
        return set_of_column_names

    def remove_duplicate_column_names(self, list_of_dict_of_header_info):
        """
        No two columns of the table can have the same data
        :param plot_options:
        :return:
        """
        list_of_column_names = []
        i = 0
        n = len(list_of_dict_of_header_info)
        while i < n:
            dict_of_header_info = list_of_dict_of_header_info[i]
            if dict_of_header_info[COLUMN_NAME] in list_of_column_names:
                del list_of_dict_of_header_info[i]
                n -= 1
            else:
                list_of_column_names.append(dict_of_header_info[COLUMN_NAME])
                i += 1
        return list_of_column_names
