# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

# selectors are dropdowns, checkboxes etc.
AVAILABLE_SELECTORS = {
    "select": {"select_html_template": "select_filter.html", "type": "filter"},
    "axis": {"select_html_template": "select_axis.html", "type": "axis"},
    "numerical_filter": {
        "select_html_template": "numerical_filter.html",
        "type": "numerical_filter",
    },
}
