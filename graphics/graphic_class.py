import json


class Graphic(object):
    def __init__(self):
        pass

    def draw(self, data, data_to_struct, plot_options):
        """

        :param data: dictionary of data
        :param data_to_struct: instructions of some kind how to put the data into plot_options
        :param plot_options: dictionary that contains all the information to make a graphic minus the data
        :return: instructions that will be passed to the html that will plot the object.
        """
        raise NotImplementedError
