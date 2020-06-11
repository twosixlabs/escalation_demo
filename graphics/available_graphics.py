from graphics.simple_plotly_plot import PlotlyPlot

AVAILABLE_GRAPHICS = {'line plot': PlotlyPlot('line'),
                      'bar plot': PlotlyPlot('bar'),
                      'barh plot': PlotlyPlot('barh'),
                      'box plot': PlotlyPlot('box'),
                      'scatter plot': PlotlyPlot('scatter')
                      }
