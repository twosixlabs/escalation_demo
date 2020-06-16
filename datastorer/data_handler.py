class DataHandler(object):
    def __init__(self):
        raise NotImplementedError

    def get_column_names(self):
        """
        What columns does the data have
        """
        raise NotImplementedError

    def get_column_data(self, cols: list) -> list:
        """

        :param cols: list of names
        :return:
        """
        raise NotImplementedError
