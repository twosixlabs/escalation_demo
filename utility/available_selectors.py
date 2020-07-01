from collections import OrderedDict
from operator import lt, le, eq, ge, gt

# selectors are dropdowns, checkboxes etc.
AVAILABLE_SELECTORS = {
    "select": {"select_html_template": "select_filter.html", "type": "filter"},
    "axis": {"select_html_template": "select_axis.html", "type": "axis"},
    "numerical_filter": {
        "select_html_template": "numerical_filter.html",
        "type": "numerical_filter",
    },
}

OPERATIONS_FOR_NUMERICAL_FILTERS = OrderedDict(
    [(">", gt), (">=", ge), ("=", eq), ("<=", le), ("<", lt)]
)
