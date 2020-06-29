from collections import defaultdict

from utility.available_selectors import AVAILABLE_SELECTORS
from utility.constants import *


def add_info_from_addendum_to_config_dict(
    single_page_config_dict: dict, addendum_dict: dict
) -> dict:
    """
    We build a page based on 2 dictonaries, what is in the config and what is submitted in the HTML form.
    :param single_page_config_dict:
    :param addendum_dict: see test_app_config_addendum.json for an example of one of these
    :return:
    """

    for graphic_index, selection_index_dict in addendum_dict.items():
        operation_list = []
        for selection_dict in selection_index_dict.values():
            # creates an operations where only the values selected along a column will be shown in the plot
            if selection_dict[OPTION_TYPE] == FILTER:
                operation_list.append(selection_dict)
            # modifies the aixs shown in the config
            elif selection_dict[OPTION_TYPE] == AXIS:
                for point_index, data_dict in single_page_config_dict[graphic_index][
                    DATA
                ].items():
                    axis = selection_dict[COLUMN_NAME]
                    data_dict[axis] = selection_dict[SELECTED]
                    single_page_config_dict[graphic_index][DATA][
                        point_index
                    ] = data_dict
            # creates an operations where only the values following an (in)equality
            # along a column will be shown in the plot
            elif selection_dict[OPTION_TYPE] == NUMERICAL_FILTER:
                # the numerical filter contains two filters so add them separately
                base_info_dict_for_selector = {
                    OPTION_TYPE: NUMERICAL_FILTER,
                    COLUMN_NAME: selection_dict[COLUMN_NAME],
                }
                for loc in [UPPER_INEQUALITY, LOWER_INEQUALITY]:
                    numerical_filter_info = selection_dict[INEQUALITY_LOC.format(loc)]
                    if numerical_filter_info[VALUE] is None:
                        continue
                    operation_list.append(
                        {**base_info_dict_for_selector, **numerical_filter_info}
                    )
        if operation_list:
            single_page_config_dict[graphic_index][DATA_FILTERS] = operation_list
    return single_page_config_dict


FILTER_SELECTION_DEFAULTS = {
    "filter": lambda selection_option, data_info: {
        OPTION_TYPE: FILTER,
        OPTION_COL: selection_option[OPTION_COL],
        SELECTED: SHOW_ALL_ROW,
    },
    "axis": lambda selection_option, data_info: {
        OPTION_TYPE: AXIS,
        OPTION_COL: selection_option[OPTION_COL],
        SELECTED: data_info[selection_option[OPTION_COL]],
    },
    "numerical_filter": lambda selection_option, data_info: {
        OPTION_TYPE: NUMERICAL_FILTER,
        OPTION_COL: selection_option[OPTION_COL],
        INEQUALITY_LOC.format(UPPER_INEQUALITY): {OPERATION: "<=", VALUE: ""},
        INEQUALITY_LOC.format(LOWER_INEQUALITY): {OPERATION: ">=", VALUE: ""},
    },
}


def make_default_addendum(single_page_config_dict: dict) -> dict:
    """
    This addendum sets the defaults for the selectors in the case that there
     is no user input submitted in the HTML form
    such as when first opening the page
    :param single_page_config_dict:
    :return:
    """
    addendum_dict = defaultdict(dict)
    for graphic_index, graphic_dict in single_page_config_dict.items():
        for selection_index, selection_option in enumerate(
            graphic_dict.get(SELECTABLE_DATA_LIST, [])
        ):
            # zero in POINTS_NUM.format(0) because
            # I am assuming that all the lines/scatters are the same along the selected axis
            addendum_dict[graphic_index][
                SELECTION_NUM.format(selection_index)
            ] = FILTER_SELECTION_DEFAULTS[
                AVAILABLE_SELECTORS[selection_option[OPTION_TYPE]][OPTION_TYPE]
            ](
                selection_option,
                single_page_config_dict[graphic_index][DATA][POINTS_NUM.format(0)],
            )

    return addendum_dict
