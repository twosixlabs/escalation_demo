import pytest

from datastorer.local_handler import LocalCSVHandler


@pytest.fixture()
def make_local_handler():
    got_data = LocalCSVHandler("tests/test_data/penguins_size_small")
    return got_data


def test_local_handler_init(make_local_handler):
    assert (
        make_local_handler.file_path
        == "tests/test_data/penguins_size_small/penguins_size_small.csv"
    )


def test_get_column_names(make_local_handler):
    cols_names = make_local_handler.get_column_names()
    assert "flipper_length_mm" in cols_names
    assert "species" in cols_names
    assert "island" in cols_names
    assert "sex" in cols_names
    assert "culmen_length_mm" in cols_names
    assert "culmen_depth_mm" in cols_names
    assert "body_mass_g" in cols_names
    assert "penguins_size" not in cols_names


# def test_get_column_data(make_local_handler):
def test_get_column_data(make_local_handler):
    data_dict = ["body_mass_g", "flipper_length_mm"]
    test_dict = make_local_handler.get_column_data(data_dict)
    assert test_dict["body_mass_g"] == [3750, 3800, 3250]
    assert test_dict["flipper_length_mm"] == [181, 186, 195]


def test_get_column_unique_entries(make_local_handler):
    unique_dict = make_local_handler.get_column_unique_entries(["sex", "island"])
    assert "MALE" in unique_dict["sex"]
    assert "FEMALE" in unique_dict["sex"]
    assert "Torgersen" in unique_dict["island"]
