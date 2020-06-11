from graphics.available_graphics import AVAILABLE_GRAPHICS


def get_graphic(graphic_name, options, data_name, col_names):
    '''
    :param graphic_name: From the dictionary of Available graphics
    :param options: To be passed in to the graphics object
    :param data_name: name of database/file to get data
    :param col_names: which columns
    :return: strings that will plot graphic
    '''

    new_graphic = AVAILABLE_GRAPHICS[graphic_name]
    data = [[3, 6, 7], [4, 8, 1]]
    new_graphic.draw(data)

    return new_graphic.draw(data)
