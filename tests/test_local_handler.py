import pytest

from datastorer.local_handler import LocalHandler


@pytest.fixture()
def make_local_handler():
    got_data = LocalHandler("tests/test_data/penguins_size.csv")
    return got_data


def test_local_handler_init(make_local_handler):
    assert make_local_handler.file_path == "tests/test_data/penguins_size.csv"


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
