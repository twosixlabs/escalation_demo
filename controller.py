from datastorer.local_handler import LocalHandler
from graphics.available_graphics import AVAILABLE_GRAPHICS


def get_graphic(graphic_name, options, data_name, col_names):
    """
    :param graphic_name: From the dictionary of Available graphics
    :param options: To be passed in to the graphics object
    :param data_name: name of database/file to get data
    :param col_names: which columns
    :return: strings that will plot graphic
    """
    new_data = LocalHandler("tests/test_data/penguins_size.csv")
    columns = ["body_mass_g", "flipper_length_mm"]
    new_graphic = AVAILABLE_GRAPHICS[graphic_name]
    testdata = new_data.get_column_data(columns)  # just to test as I get functionality
    [filename, jsonstr] = new_graphic.draw(testdata, columns)
    htmldata = dict(plot=jsonstr, cols=new_data.get_column_names())

    return filename, htmldata
