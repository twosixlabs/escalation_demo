# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

# selectors are dropdowns, checkboxes etc.
from utility.constants import SELECT_HTML_TEMPLATE, SELECTOR_TYPE, TEXT

AVAILABLE_SELECTORS = {
    "select": {
        SELECT_HTML_TEMPLATE: "selector.html",
        SELECTOR_TYPE: "filter",
        TEXT: "Filter by {}",
    },
    "axis": {
        SELECT_HTML_TEMPLATE: "selector.html",
        SELECTOR_TYPE: "axis",
        TEXT: "{} axis",
    },
    "groupby": {
        SELECT_HTML_TEMPLATE: "selector.html",
        SELECTOR_TYPE: "groupby",
        TEXT: "Group by:",
    },
    "numerical_filter": {
        SELECT_HTML_TEMPLATE: "numerical_filter.html",
        SELECTOR_TYPE: "numerical_filter",
        TEXT: "Filter by {}",
    },
}
