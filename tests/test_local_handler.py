import pandas as pd

from datastorer.local_handler import LocalCSVHandler
from utility.constants import (
    SELECTOR_TYPE,
    FILTER,
    NUMERICAL_FILTER,
    OPERATION,
    VALUE,
    INEQUALITIES,
    DATA_SOURCE_TYPE,
    DATA_LOCATION,
)


def test_local_handler_init(local_handler_fixture_small):
    data_sources = local_handler_fixture_small.data_sources
    assert len(data_sources) == 1
    first_data_source = data_sources[0]
    assert (
        first_data_source[DATA_LOCATION]
        == "tests/test_data/penguin_size_small/penguin_size_small.csv"
    )
    # todo: more complicated init with key joining


def test_get_column_names(local_handler_fixture_small):
    cols_names = local_handler_fixture_small.get_column_names()
    assert "penguin_size_small.flipper_length_mm" in cols_names
    assert "penguin_size_small.species" in cols_names
    assert "penguin_size_small.island" in cols_names
    assert "penguin_size_small.sex" in cols_names
    assert "penguin_size_small.culmen_length_mm" in cols_names
    assert "penguin_size_small.culmen_depth_mm" in cols_names
    assert "penguin_size_small.body_mass_g" in cols_names
    assert "penguin_size_small.penguin_size" not in cols_names


def test_get_column_data(local_handler_fixture_small):
    data_dict = [
        "penguin_size_small.body_mass_g",
        "penguin_size_small.flipper_length_mm",
    ]
    test_dict = local_handler_fixture_small.get_column_data(data_dict)
    assert test_dict["penguin_size_small.body_mass_g"] == [3750, 3800, 3250]
    assert test_dict["penguin_size_small.flipper_length_mm"] == [181, 186, 195]

    test_dict = local_handler_fixture_small.get_column_data(
        data_dict,
        [{"type": "filter", "column": "penguin_size_small.sex", "selected": ["MALE"]}],
    )
    assert test_dict["penguin_size_small.body_mass_g"] == [3750]
    assert test_dict["penguin_size_small.flipper_length_mm"] == [181]

    test_dict = local_handler_fixture_small.get_column_data(
        data_dict,
        [
            {
                "type": "numerical_filter",
                "column": "penguin_size_small.body_mass_g",
                "operation": ">",
                "value": 3250,
            }
        ],
    )

    assert test_dict["penguin_size_small.body_mass_g"] == [3750, 3800]
    assert test_dict["penguin_size_small.flipper_length_mm"] == [181, 186]


def test_get_column_unique_entries(local_handler_fixture_small):
    unique_dict = local_handler_fixture_small.get_column_unique_entries(
        ["penguin_size_small.sex", "penguin_size_small.island"]
    )
    assert "MALE" in unique_dict["penguin_size_small.sex"]
    assert "FEMALE" in unique_dict["penguin_size_small.sex"]
    assert "Torgersen" in unique_dict["penguin_size_small.island"]


# define 2 joined data tables as the data_source
TWO_DATA_SOURCES_CONFIG = [
    {"data_source_type": "penguin_size"},
    {
        "data_source_type": "mean_penguin_stat",
        "left_keys": [
            "penguin_size.study_name",
            "penguin_size.sex",
            "penguin_size.species",
        ],
        "right_keys": [
            "mean_penguin_stat.study_name",
            "mean_penguin_stat.sex",
            "mean_penguin_stat.species",
        ],
    },
]


def test_init(test_app_client):
    handler = LocalCSVHandler(data_sources=TWO_DATA_SOURCES_CONFIG)
    # test that init gets the correct file for each data source folder
    assert (
        handler.data_sources[0][DATA_LOCATION]
        == "tests/test_data/penguin_size/penguin_size.csv"
    )
    assert (
        handler.data_sources[1][DATA_LOCATION]
        == "tests/test_data/mean_penguin_stat/mean_penguin_stat.csv"
    )


def test_build_combined_data_table(test_app_client):
    handler = LocalCSVHandler(data_sources=TWO_DATA_SOURCES_CONFIG)
    mean_penguin_stats = pd.read_csv(handler.data_sources[0][DATA_LOCATION])
    num_rows_in_leftmost_table = mean_penguin_stats.shape[0]
    num_rows_in_combined_table = handler.combined_data_table.shape[0]
    # this is a left join, so assuming only one matching key in right table per key in left,
    # the number of rows of final table should equal the left/first table
    assert num_rows_in_leftmost_table == num_rows_in_combined_table
    # todo: one to many join, where we expect the number of rows to change
