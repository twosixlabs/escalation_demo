from collections import defaultdict

from werkzeug.datastructures import ImmutableMultiDict

from utility.available_selectors import AVAILABLE_SELECTORS
from utility.constants import *

NUMERICAL_FILTER_DEFAULT = {
    UPPER_INEQUALITY: {OPERATION: "<=", VALUE: ""},
    LOWER_INEQUALITY: {OPERATION: ">=", VALUE: ""},
}


def add_instructions_to_config_dict(
    single_page_graphic_config_dict: dict, addendum_dict: ImmutableMultiDict = None
) -> dict:
    """
    We build a page based on 2 dictonaries, what is in the config and what is submitted in the HTML form.
    :param single_page_graphic_config_dict:
    :param addendum_dict: e.g ImmutableMultiDict([('graphic_index', 'graphic_0'), ('selection_0', 'SHOW_ALL_ROW'),
     ('selection_2_upper_operation', '<='), ('selection_2_upper_value', '4'))])
    Should not pass an empty ImmutableMultiDict
    :return: modified single_page_config_dict
    """
    if addendum_dict is None:
        addendum_dict = ImmutableMultiDict()

    for graphic_index, graphic_dict in single_page_graphic_config_dict.items():
        if SELECTABLE_DATA_LIST in graphic_dict:
            selector_list = graphic_dict[SELECTABLE_DATA_LIST]
            data_info_dict = graphic_dict[DATA]
            add_active_selectors_to_selectable_data_list(
                selector_list, data_info_dict, addendum_dict
            )
            if addendum_dict.get(GRAPHIC_INDEX) == graphic_index:
                graphic_dict[DATA_FILTERS] = add_operations_to_the_data(
                    selector_list, data_info_dict, addendum_dict
                )
    return single_page_graphic_config_dict


def add_active_selectors_to_selectable_data_list(
    selectable_data_list: list,
    data_info_dict: dict,
    addendum_dict: ImmutableMultiDict = None,
) -> dict:
    """
    Sets which selectors are active based on user choices.
    If none have been selected sets reasonable defaults
    :param selectable_data_list: each element of the list is a dictionary on how to build the selector on the webpage
    :param data_info_dict: Dictionary that has which data goes in which plot
    :param addendum_dict: User selections form the webpage
    :return:
    """

    if addendum_dict is None:
        addendum_dict = ImmutableMultiDict()
    for selection_index, selection_dict in enumerate(selectable_data_list):
        if selection_dict[SELECTOR_TYPE] == SELECTOR:
            # getlist does not not work like get so need to set default "manually"

            selection_index_str = SELECTION_NUM.format(selection_index)
            selection_dict[ACTIVE_SELECTORS] = addendum_dict.getlist(
                selection_index_str
            ) or [SHOW_ALL_ROW]
        elif selection_dict[SELECTOR_TYPE] == AXIS:
            # in the case of no user selected the active selector is the one currently being plotted,
            # taken from the first set of points (index 0)
            selection_dict[ACTIVE_SELECTORS] = addendum_dict.get(
                SELECTION_NUM.format(selection_index),
                data_info_dict[POINTS_NUM.format(0)][selection_dict[COLUMN_NAME]],
            )
        elif selection_dict[SELECTOR_TYPE] == NUMERICAL_FILTER:
            locations = [UPPER_INEQUALITY, LOWER_INEQUALITY]
            active_numerical_filter_dict = defaultdict(dict)
            for loc in locations:
                for input_type in [OPERATION, VALUE]:
                    # pull the relevant filter info from the submitted form
                    active_numerical_filter_dict[loc][input_type] = addendum_dict.get(
                        SELECTION_NUM_LOC_TYPE.format(selection_index, loc, input_type),
                        NUMERICAL_FILTER_DEFAULT[loc][input_type],
                    )
            selection_dict[ACTIVE_SELECTORS] = active_numerical_filter_dict


def add_operations_to_the_data(
    selectable_data_list: list, data_info_dict: dict, addendum_dict: ImmutableMultiDict
) -> list:
    """
    Adds operations to be passed to the data handlers for the data
    :param selectable_data_list: each element of the list is a dictionary on how to build the selector on the webpage
    :param data_info_dict: Dictionary that has which data goes in which plot
    :param addendum_dict: User selections form the webpage
    :return:
    """
    operation_list = []
    for selection_index, selection_dict in enumerate(selectable_data_list):
        selection_index_str = SELECTION_NUM.format(selection_index)
        option_type = AVAILABLE_SELECTORS[selection_dict[SELECTOR_TYPE]][OPTION_TYPE]

        base_info_dict_for_selector = {
            OPTION_TYPE: option_type,
            COLUMN_NAME: selection_dict[COLUMN_NAME],
        }
        # creates an operations where only the values selected along a column will be shown in the plot
        if option_type == FILTER:
            selection = addendum_dict.getlist(selection_index_str)
            if len(selection) == 0 or SHOW_ALL_ROW in selection:
                continue
            base_info_dict_for_selector[SELECTED] = selection
            operation_list.append(base_info_dict_for_selector)
        # modifies the axis shown in the config
        elif option_type == AXIS:
            new_column_for_axis = addendum_dict.get(selection_index_str)
            axis = selection_dict[COLUMN_NAME]
            for line_index, axis_dict in data_info_dict.items():
                axis_dict[axis] = new_column_for_axis
        # creates an operations where only the values following an (in)equality
        # along a column will be shown in the plot
        elif option_type == NUMERICAL_FILTER:
            # the numerical filter contains two filters so add them separately
            for loc in [UPPER_INEQUALITY, LOWER_INEQUALITY]:
                # get the value submitted in the web form by using its name
                # format specified in numeric_filter.html
                numerical_value = addendum_dict[
                    SELECTION_NUM_LOC_TYPE.format(selection_index, loc, VALUE)
                ]
                if numerical_value == "":
                    continue
                numerical_filter_info = {
                    VALUE: float(numerical_value),
                    OPERATION: addendum_dict[
                        SELECTION_NUM_LOC_TYPE.format(selection_index, loc, OPERATION)
                    ],
                }
                operation_list.append(
                    {**base_info_dict_for_selector, **numerical_filter_info}
                )
    return operation_list
