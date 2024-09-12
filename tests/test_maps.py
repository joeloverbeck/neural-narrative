from unittest.mock import Mock

import pytest

from src.enums import PlaceType
from src.maps.abstracts.abstract_factories import CurrentPlaceFactory
from src.maps.abstracts.factory_products import CurrentPlaceProduct
from src.maps.maps import is_current_place_a_place_type


# Assuming the code above is imported

def test_is_current_place_a_place_type_valid_place():
    # Mock CurrentPlaceProduct
    mock_place_product = Mock(spec=CurrentPlaceProduct)
    mock_place_product.get.return_value = {"type": "location", "place_template": "eidolon arcade", "area": "1",
                                           "characters": []}
    mock_place_product.is_valid.return_value = True

    # Mock CurrentPlaceFactory
    mock_place_factory = Mock(spec=CurrentPlaceFactory)
    mock_place_factory.create_current_place.return_value = mock_place_product

    # Test with PlaceType.LOCATION (which matches "location" in the dict)
    assert is_current_place_a_place_type(PlaceType.LOCATION, mock_place_factory)


def test_is_current_place_a_place_type_invalid_place():
    # Mock CurrentPlaceProduct
    mock_place_product = Mock(spec=CurrentPlaceProduct)
    mock_place_product.get.return_value = {"type": "region", "place_template": "eidolon arcade", "area": "1",
                                           "characters": []}
    mock_place_product.is_valid.return_value = True

    # Mock CurrentPlaceFactory
    mock_place_factory = Mock(spec=CurrentPlaceFactory)
    mock_place_factory.create_current_place.return_value = mock_place_product

    # Test with PlaceType.LOCATION (which does not match "region")
    assert not is_current_place_a_place_type(PlaceType.LOCATION, mock_place_factory)


def test_is_current_place_a_place_type_invalid_product():
    # Mock CurrentPlaceProduct
    mock_place_product = Mock(spec=CurrentPlaceProduct)
    mock_place_product.is_valid.return_value = False
    mock_place_product.get_error.return_value = "Invalid place"

    # Mock CurrentPlaceFactory
    mock_place_factory = Mock(spec=CurrentPlaceFactory)
    mock_place_factory.create_current_place.return_value = mock_place_product

    # Test to check if ValueError is raised for invalid place product
    with pytest.raises(ValueError, match="Was unable to produce the current place data: Invalid place"):
        is_current_place_a_place_type(PlaceType.LOCATION, mock_place_factory)
