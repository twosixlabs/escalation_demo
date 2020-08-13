from wizard_ui.wizard_utils import invert_dict_lists


def test_invert_dict_lists():
    test_dict = {"a": [1], "b": [2, 3]}
    expected_dict = {1: "a", 2: "b", 3: "b"}
    inverted_dict = invert_dict_lists(test_dict)
    assert inverted_dict == expected_dict
