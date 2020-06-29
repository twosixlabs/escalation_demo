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
    assert False
