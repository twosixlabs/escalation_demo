from graphics.plotly_plot import PlotlyPlot
import pytest
import json

TITLE1 = "random_num"
TITLE2 = "another_rand"


@pytest.fixture()
def make_data():
    data = {TITLE1: [3, 6, 7], TITLE2: [4, 8, 1]}

    return data


def test_plotly_draw_scatter(make_data):

    options = {"data": [{"type": "scatter", "mode": "markers"}]}
    test = PlotlyPlot()
    data_to_struct = [{"x": TITLE2, "y": TITLE1}]
    json_output = test.draw(make_data, data_to_struct, options)
    options_dict = json.loads(json_output)
    assert options_dict["data"][0]["type"] == "scatter"
    assert options_dict["data"][0]["x"] == make_data[TITLE2]
    assert options_dict["data"][0]["y"] == make_data[TITLE1]
    assert options_dict["data"][0]["mode"] == options["data"][0]["mode"]
    assert options_dict["layout"]["xaxis"]["title"] == TITLE2
    assert options_dict["layout"]["yaxis"]["title"] == TITLE1
