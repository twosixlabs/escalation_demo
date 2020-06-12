from graphics.plotly_plot import PlotlyPlot
import pytest
import json


@pytest.fixture()
def make_data():
    data = [[3, 6, 7], [4, 8, 1]]
    data_names = ["x", "y"]
    return data, data_names


def test_plotly_draw(make_data):
    def sub_test(test, type):
        [data, data_names] = make_data
        [filename, json_output] = test.draw(data, data_names)
        options_dict = json.loads(json_output)
        expected_file_name = "datalayout.html"
        assert filename == expected_file_name
        assert options_dict["data"][0]["type"] == type
        assert options_dict["data"][0]["x"] == data[0]
        assert options_dict["data"][0]["y"] == data[1]
        assert options_dict["layout"]["xaxis"]["title"] == data_names[0]
        assert options_dict["layout"]["yaxis"]["title"] == data_names[1]

    # I am going to use a scatter plot as an example
    test = PlotlyPlot("scatter")
    sub_test(test, "scatter")

    test = PlotlyPlot("bar")
    sub_test(test, "bar")
