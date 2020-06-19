class DataHandler(object):
    # todo: enforce that the function signatures on the children classes are the same as here, to make childern classes interchangeable
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

    def get_column_unique_entries(self, cols: list) -> dict:
        """

        :param cols: list of names
        :return:
        """
        raise NotImplementedError
