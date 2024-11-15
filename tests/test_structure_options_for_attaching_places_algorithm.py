# test_structure_options_for_attaching_places_algorithm.py

import logging

import pytest

from src.maps.algorithms.structure_options_for_attaching_places_algorithm import (
    StructureOptionsForAttachingPlacesAlgorithm,
)


@pytest.fixture
def sample_dict_items():
    return [
        {"value": "1", "display": "Terra Firma"},
        {"value": "2", "display": "Euskal Herria"},
        {"value": "3", "display": "Donostia"},
        {"value": "4", "display": "Old Quarter apartment building"},
        {"value": "10", "display": "La Concha Bay"},
        {"value": "11", "display": "Mar y Sazón"},
        {"value": "12", "display": "Secret Cove"},
    ]


@pytest.fixture
def sample_string_items():
    return [
        "The Peninsula Garden",
        "Villa Opulencia",
        "Villa Sombra",
        "The Whispered Secret",
        "FNAC",
        "Komisaria Donostia",
        "The Observer's Chamber",
        "The Epicurean's Gallery",
        "The Gothic Chamber of Reflection",
        "The Contemplative Corner",
        "The Master Bedroom",
        "The Single Mother's Sanctuary",
    ]


def test_all_dicts_default_attributes(sample_dict_items, caplog):
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(items=sample_dict_items)
    expected_output = [
        {"value": item["value"], "display": item["display"]}
        for item in sample_dict_items
    ]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    for item in sample_dict_items:
        expected_log = f"Dict item - Value: {item['value']}, Display: {item['display']}"
        assert expected_log in caplog.text


def test_all_dicts_custom_attributes(caplog):
    custom_items = [
        {"id": "100", "name": "Alpha"},
        {"id": "200", "name": "Beta"},
    ]
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(
        items=custom_items, value_attr="id", display_attr="name"
    )
    expected_output = [
        {"value": item["id"], "display": item["name"]} for item in custom_items
    ]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    for item in custom_items:
        expected_log = f"Dict item - Value: {item['id']}, Display: {item['name']}"
        assert expected_log in caplog.text


def test_mixed_items_default_attributes(sample_dict_items, sample_string_items, caplog):
    mixed_items = sample_dict_items + sample_string_items
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(items=mixed_items)

    expected_output = [
        {"value": item["value"], "display": item["display"]}
        for item in sample_dict_items
    ]
    expected_output += [
        {"value": item, "display": item} for item in sample_string_items
    ]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    for item in sample_dict_items:
        expected_log = f"Dict item - Value: {item['value']}, Display: {item['display']}"
        assert expected_log in caplog.text

    for item in sample_string_items:
        expected_log = f"String item - Value: {item}, Display: {item}"
        assert expected_log in caplog.text


def test_mixed_items_custom_attributes(caplog):
    custom_dict_items = [
        {"id": "100", "name": "Alpha"},
        {"id": "200", "name": "Beta"},
    ]
    string_items = ["Gamma", "Delta"]
    mixed_items = custom_dict_items + string_items

    algorithm = StructureOptionsForAttachingPlacesAlgorithm(
        items=mixed_items, value_attr="id", display_attr="name"
    )

    expected_output = [
        {"value": item["id"], "display": item["name"]} for item in custom_dict_items
    ]
    expected_output += [{"value": item, "display": item} for item in string_items]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    for item in custom_dict_items:
        expected_log = f"Dict item - Value: {item['id']}, Display: {item['name']}"
        assert expected_log in caplog.text

    for item in string_items:
        expected_log = f"String item - Value: {item}, Display: {item}"
        assert expected_log in caplog.text


def test_all_strings(sample_string_items, caplog):
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(items=sample_string_items)
    expected_output = [{"value": item, "display": item} for item in sample_string_items]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    for item in sample_string_items:
        expected_log = f"String item - Value: {item}, Display: {item}"
        assert expected_log in caplog.text


def test_empty_items(caplog):
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(items=[])
    expected_output = []

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output
    assert "Dict item" not in caplog.text
    assert "String item" not in caplog.text


def test_dicts_missing_attributes(caplog):
    items = [
        {"value": "1"},  # Missing 'display'
        {"display": "Only Display"},  # Missing 'value'
        {},  # Missing both
    ]
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(items=items)
    expected_output = [
        {"value": "1", "display": ""},
        {"value": "", "display": "Only Display"},
        {"value": "", "display": ""},
    ]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    expected_logs = [
        "Dict item - Value: 1, Display: ",
        "Dict item - Value: , Display: Only Display",
        "Dict item - Value: , Display: ",
    ]
    for log_msg in expected_logs:
        assert log_msg in caplog.text


def test_custom_attributes_missing_in_some_dicts(caplog):
    items = [
        {"id": "100", "name": "Alpha"},
        {"id": "200"},  # Missing 'name'
        {"name": "Gamma"},  # Missing 'id'
        {},  # Missing both
    ]
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(
        items=items, value_attr="id", display_attr="name"
    )
    expected_output = [
        {"value": "100", "display": "Alpha"},
        {"value": "200", "display": ""},
        {"value": "", "display": "Gamma"},
        {"value": "", "display": ""},
    ]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    expected_logs = [
        "Dict item - Value: 100, Display: Alpha",
        "Dict item - Value: 200, Display: ",
        "Dict item - Value: , Display: Gamma",
        "Dict item - Value: , Display: ",
    ]
    for log_msg in expected_logs:
        assert log_msg in caplog.text


def test_items_with_empty_strings(caplog):
    items = [
        "",
        "Valid String",
        "",
    ]
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(items=items)
    expected_output = [
        {"value": "", "display": ""},
        {"value": "Valid String", "display": "Valid String"},
        {"value": "", "display": ""},
    ]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    expected_logs = [
        "String item - Value: , Display: ",
        "String item - Value: Valid String, Display: Valid String",
        "String item - Value: , Display: ",
    ]
    for log_msg in expected_logs:
        assert log_msg in caplog.text


def test_logging_when_custom_attributes_not_present(caplog):
    items = [
        {"id": "100", "name": "Alpha"},
        {"id": "200"},  # Missing 'name'
        {"name": "Gamma"},  # Missing 'id'
    ]
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(
        items=items, value_attr="id", display_attr="name"
    )
    expected_output = [
        {"value": "100", "display": "Alpha"},
        {"value": "200", "display": ""},
        {"value": "", "display": "Gamma"},
    ]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    expected_logs = [
        "Dict item - Value: 100, Display: Alpha",
        "Dict item - Value: 200, Display: ",
        "Dict item - Value: , Display: Gamma",
    ]
    for log_msg in expected_logs:
        assert log_msg in caplog.text


def test_logging_correctly_identifies_item_types(caplog):
    items = [
        {"value": "1", "display": "Terra Firma"},
        "The Peninsula Garden",
        {"value": "2", "display": "Euskal Herria"},
        "Villa Opulencia",
    ]
    algorithm = StructureOptionsForAttachingPlacesAlgorithm(items=items)

    expected_output = [
        {"value": "1", "display": "Terra Firma"},
        {"value": "The Peninsula Garden", "display": "The Peninsula Garden"},
        {"value": "2", "display": "Euskal Herria"},
        {"value": "Villa Opulencia", "display": "Villa Opulencia"},
    ]

    with caplog.at_level(logging.INFO):
        result = algorithm.do_algorithm()

    assert result == expected_output

    expected_logs = [
        "Dict item - Value: 1, Display: Terra Firma",
        "String item - Value: The Peninsula Garden, Display: The Peninsula Garden",
        "Dict item - Value: 2, Display: Euskal Herria",
        "String item - Value: Villa Opulencia, Display: Villa Opulencia",
    ]
    for log_msg in expected_logs:
        assert log_msg in caplog.text
