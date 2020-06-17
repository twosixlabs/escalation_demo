import pytest

from datastorer.local_handler import LocalHandler


@pytest.fixture()
def make_local_handler():
    got_data = LocalHandler("tests/test_data/penguins_size_small.csv")
    return got_data


def test_local_handler_init(make_local_handler):
    assert make_local_handler.file_path == "tests/test_data/penguins_size_small.csv"


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
    data_dict = {"x": "body_mass_g", "y": "flipper_length_mm"}
    test_dict = make_local_handler.get_column_data(data_dict)
    assert (test_dict["x"] == [3750, 3800, 3250]).all()
    assert (test_dict["y"] == [181, 186, 195]).all()
