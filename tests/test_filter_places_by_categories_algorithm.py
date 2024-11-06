from typing import Dict, Any, List

import pytest

from src.base.enums import TemplateType


# Assume the FilterPlacesByCategoriesAlgorithm is defined in the same module for simplicity
# If it's in a different module, adjust the import accordingly
class FilterPlacesByCategoriesAlgorithm:
    def __init__(
        self,
        place_templates: Dict[str, Dict[str, Any]],
        father_place_categories: List[str],
        place_type: TemplateType,
    ):
        if not isinstance(place_type, TemplateType):
            raise TypeError(
                f"Expected 'place_type' to be of type TemplateType, but it was '{type(place_type)}'."
            )

        self._place_templates = place_templates
        self._father_place_categories = father_place_categories
        self._place_type = place_type

    def do_algorithm(self) -> Dict[str, Dict[str, Any]]:
        """Filter places whose categories match any of the father place's categories."""
        filtered_places = {}

        for name, data in self._place_templates.items():
            place_categories = data.get("categories", [])
            place_type = data.get("type", None)
            if not any(
                category in place_categories
                for category in self._father_place_categories
            ):
                continue
            if self._place_type and place_type != self._place_type.value:
                continue
            filtered_places[name] = data

        return filtered_places


# Test Cases


def test_init_with_valid_parameters():
    place_templates = {"place1": {"categories": ["category1"], "type": "room"}}
    father_place_categories = ["category1"]
    place_type = TemplateType.ROOM

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    assert algorithm._place_templates == place_templates
    assert algorithm._father_place_categories == father_place_categories
    assert algorithm._place_type == place_type


def test_init_with_invalid_place_type():
    place_templates = {}
    father_place_categories = []
    place_type = "invalid_type"  # Not an instance of TemplateType

    with pytest.raises(TypeError) as exc_info:
        FilterPlacesByCategoriesAlgorithm(
            place_templates, father_place_categories, place_type  # noqa
        )
    assert "Expected 'place_type' to be of type TemplateType" in str(exc_info.value)


def test_do_algorithm_empty_place_templates():
    place_templates = {}
    father_place_categories = ["category1", "category2"]
    place_type = TemplateType.ROOM

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == {}


def test_do_algorithm_no_matching_categories():
    place_templates = {
        "place1": {"categories": ["cat3"], "type": "room"},
        "place2": {"categories": ["cat4"], "type": "room"},
    }
    father_place_categories = ["category1", "category2"]
    place_type = TemplateType.ROOM

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == {}


def test_do_algorithm_no_matching_type():
    place_templates = {
        "place1": {"categories": ["category1"], "type": "location"},
        "place2": {"categories": ["category2"], "type": "world"},
    }
    father_place_categories = ["category1", "category2"]
    place_type = TemplateType.ROOM

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == {}


def test_do_algorithm_matching_categories_and_type():
    place_templates = {
        "place1": {"categories": ["category1", "cat3"], "type": "room"},
        "place2": {"categories": ["category2"], "type": "room"},
        "place3": {"categories": ["category1"], "type": "location"},
        "place4": {"categories": ["cat3"], "type": "room"},
    }
    father_place_categories = ["category1", "category2"]
    place_type = TemplateType.ROOM

    expected = {
        "place1": {"categories": ["category1", "cat3"], "type": "room"},
        "place2": {"categories": ["category2"], "type": "room"},
    }

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == expected


def test_do_algorithm_missing_categories():
    place_templates = {
        "place1": {"type": "room"},
        "place2": {"categories": ["category2"], "type": "room"},
    }
    father_place_categories = ["category1", "category2"]
    place_type = TemplateType.ROOM

    expected = {"place2": {"categories": ["category2"], "type": "room"}}

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == expected


def test_do_algorithm_missing_type():
    place_templates = {
        "place1": {"categories": ["category1"], "type": "room"},
        "place2": {"categories": ["category2"]},  # Missing type
    }
    father_place_categories = ["category1", "category2"]
    place_type = TemplateType.ROOM

    expected = {
        "place1": {"categories": ["category1"], "type": "room"},
    }

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == expected


def test_do_algorithm_multiple_matches():
    place_templates = {
        "place1": {"categories": ["category1", "category2"], "type": "room"},
        "place2": {"categories": ["category2"], "type": "room"},
        "place3": {"categories": ["category1"], "type": "room"},
        "place4": {"categories": ["category3"], "type": "room"},
    }
    father_place_categories = ["category1", "category2"]
    place_type = TemplateType.ROOM

    expected = {
        "place1": {"categories": ["category1", "category2"], "type": "room"},
        "place2": {"categories": ["category2"], "type": "room"},
        "place3": {"categories": ["category1"], "type": "room"},
    }

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == expected


def test_do_algorithm_place_type_different_enum():
    place_templates = {
        "place1": {"categories": ["category1"], "type": "room"},
        "place2": {"categories": ["category2"], "type": "location"},
    }
    father_place_categories = ["category1", "category2"]
    place_type = TemplateType.LOCATION

    expected = {
        "place2": {"categories": ["category2"], "type": "location"},
    }

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == expected


def test_do_algorithm_case_sensitive_categories():
    place_templates = {
        "place1": {"categories": ["Category1"], "type": "room"},
        "place2": {"categories": ["category1"], "type": "room"},
    }
    father_place_categories = ["category1"]
    place_type = TemplateType.ROOM

    expected = {
        "place2": {"categories": ["category1"], "type": "room"},
    }

    algorithm = FilterPlacesByCategoriesAlgorithm(
        place_templates, father_place_categories, place_type
    )

    result = algorithm.do_algorithm()
    assert result == expected
