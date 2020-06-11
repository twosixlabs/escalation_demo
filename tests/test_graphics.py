from graphics.simple_plotly_plot import PlotlyPlot


def test_plotly_draw():
    # I am going to use a scatter plot as an example
    data = [[3, 6, 7], [4, 8, 1]]
    test = PlotlyPlot('scatter')
    [filename, json] = test.draw(data)

    expected_json = '{"data": [{"x": [3, 6, 7], "y": [4, 8, 1], "type": "scatter"}], "layout": {"title": "test graph"}}'
    expected_file_name = 'plotly.html'
    assert filename == expected_file_name
    assert json == expected_json
