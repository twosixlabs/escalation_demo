from operator import eq

from utility.available_selectors import OPERATIONS_FOR_NUMERICAL_FILTERS
from utility.constants import (
    SELECTOR_TYPE,
    FILTER,
    SELECTED,
    NUMERICAL_FILTER,
    OPERATION,
    VALUE,
)


def filter_operation(data_column, filter_dict):
    if filter_dict[SELECTOR_TYPE] == FILTER:
        entry_values_to_be_shown_in_plot = filter_dict[SELECTED]
        # data storers handle a single value different from multiple values
        if len(entry_values_to_be_shown_in_plot) > 1:
            return data_column.isin(entry_values_to_be_shown_in_plot)
        else:
            return eq(data_column, entry_values_to_be_shown_in_plot[0])
    elif filter_dict[SELECTOR_TYPE] == NUMERICAL_FILTER:
        operation_function = OPERATIONS_FOR_NUMERICAL_FILTERS[filter_dict[OPERATION]]
        return operation_function(data_column, filter_dict[VALUE])
