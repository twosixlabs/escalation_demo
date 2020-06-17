from graphics.plotly_plot import PlotlyPlot
import pytest
import json


@pytest.fixture()
def make_data():
    data = {"x": [3, 6, 7], "y": [4, 8, 1]}

    return data


def test_plotly_draw_scatter(make_data):

    options = {
        "data": [{"type": "scatter", "mode": "markers"}],
        "layout": {
            "title": "test",
            "xaxis": {"title": "testx"},
            "yaxis": {"title": "testy"},
        },
    }
    test = PlotlyPlot()
    data_to_struct = {"x": ["data", 0, "x"], "y": ["data", 0, "y"]}
    json_output = test.draw(make_data, data_to_struct, options)
    options_dict = json.loads(json_output)
    assert options_dict["data"][0]["type"] == "scatter"
    assert options_dict["data"][0]["x"] == make_data["x"]
    assert options_dict["data"][0]["y"] == make_data["y"]
    assert options_dict["data"][0]["mode"] == options["data"][0]["mode"]
    assert (
        options_dict["layout"]["xaxis"]["title"] == options["layout"]["xaxis"]["title"]
    )
    assert (
        options_dict["layout"]["yaxis"]["title"] == options["layout"]["yaxis"]["title"]
    )
