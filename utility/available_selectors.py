# selectors are dropdowns, checkboxes etc.
from collections import OrderedDict

AVAILABLE_SELECTORS = {
    "select": {"select_html_template": "select_filter.html", "type": "filter"},
    "axis": {"select_html_template": "select_axis.html", "type": "axis"},
    "numerical_filter": {
        "select_html_template": "numerical_filter.html",
        "type": "numerical_filter",
    },
}

OPERATIONS_FOR_NUMERICAL_FILTERS = OrderedDict(
    [
        (">", lambda df_col, value: df_col > value),
        (">=", lambda df_col, value: df_col >= value),
        ("=", lambda df_col, value: df_col == value),
        ("<=", lambda df_col, value: df_col <= value),
        ("<", lambda df_col, value: df_col < value),
    ]
)
