import json


class Graphic(object):
    def __init__(self):
        self.options = []

    def draw(self, data, axis_names):
        """
        This function will make the graphic
        """
        raise NotImplementedError

    def update_graphic(self, data):
        """
        This will allow the user to change the data the axis are using
        :return:
        """
        raise NotImplementedError

    def get_options(self):
        """
        This function will tell what input the graphic needs to get from the user, as well as how man columns of data it can use
        :return:
        """
        raise NotImplementedError
