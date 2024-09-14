from unittest.mock import Mock

import pytest

from src.enums import PlaceType
from src.maps.map_manager import MapManager


def test_get_place_full_data_valid_location():
    # Mock FilesystemManager
    filesystem_manager = Mock()

    # Sample data
    map_file = {
        'loc1': {
            'type': 'location',
            'place_template': 'cave',
            'area': 'area1'
        },
        'area1': {
            'type': 'area',
            'place_template': 'forest',
            'region': 'region1'
        },
        'region1': {
            'type': 'region',
            'place_template': 'kingdom'
        }
    }
    location_templates = {
        'cave': {
            'description': 'A dark cave'
        }
    }
    area_templates = {
        'forest': {
            'description': 'A lush forest'
        }
    }
    region_templates = {
        'kingdom': {
            'description': 'A vast kingdom'
        }
    }

    # Mock methods to return sample data
    filesystem_manager.load_existing_or_new_json_file.side_effect = lambda path: (
        map_file if 'map' in path else
        location_templates if 'locations_template' in path else
        area_templates if 'areas_template' in path else
        region_templates if 'regions_template' in path else {}
    )
    filesystem_manager.get_file_path_to_map.return_value = 'map'
    filesystem_manager.get_file_path_to_locations_template_file.return_value = 'locations_template'
    filesystem_manager.get_file_path_to_areas_template_file.return_value = 'areas_template'
    filesystem_manager.get_file_path_to_regions_template_file.return_value = 'regions_template'

    # Instantiate MapManager with the mocked filesystem_manager
    map_manager = MapManager('playthrough_name', filesystem_manager)

    # Replace PlaceType with the mocked one
    map_manager.PlaceType = PlaceType

    # Call the method
    result = map_manager.get_place_full_data('loc1')

    # Expected result
    expected_result = {
        'location_data': {
            'name': 'cave',
            'description': 'A dark cave'
        },
        'area_data': {
            'name': 'forest',
            'description': 'A lush forest'
        },
        'region_data': {
            'name': 'kingdom',
            'description': 'A vast kingdom'
        }
    }

    assert result == expected_result


def test_get_place_full_data_valid_area():
    # Mock FilesystemManager
    filesystem_manager = Mock()

    # Sample data
    map_file = {
        'area1': {
            'type': 'area',
            'place_template': 'forest',
            'region': 'region1'
        },
        'region1': {
            'type': 'region',
            'place_template': 'kingdom'
        }
    }
    area_templates = {
        'forest': {
            'description': 'A lush forest'
        }
    }
    region_templates = {
        'kingdom': {
            'description': 'A vast kingdom'
        }
    }

    # Mock methods
    filesystem_manager.load_existing_or_new_json_file.side_effect = lambda path: (
        map_file if 'map' in path else
        area_templates if 'areas_template' in path else
        region_templates if 'regions_template' in path else {}
    )
    filesystem_manager.get_file_path_to_map.return_value = 'map'
    filesystem_manager.get_file_path_to_areas_template_file.return_value = 'areas_template'
    filesystem_manager.get_file_path_to_regions_template_file.return_value = 'regions_template'

    # Instantiate MapManager
    map_manager = MapManager('playthrough_name', filesystem_manager)
    map_manager.PlaceType = PlaceType

    # Call the method
    result = map_manager.get_place_full_data('area1')

    # Expected result
    expected_result = {
        'location_data': None,
        'area_data': {
            'name': 'forest',
            'description': 'A lush forest'
        },
        'region_data': {
            'name': 'kingdom',
            'description': 'A vast kingdom'
        }
    }

    assert result == expected_result


def test_get_place_full_data_valid_region():
    # Mock FilesystemManager
    filesystem_manager = Mock()

    # Sample data
    map_file = {
        'region1': {
            'type': 'region',
            'place_template': 'kingdom'
        }
    }
    region_templates = {
        'kingdom': {
            'description': 'A vast kingdom'
        }
    }

    # Mock methods
    filesystem_manager.load_existing_or_new_json_file.side_effect = lambda path: (
        map_file if 'map' in path else
        region_templates if 'regions_template' in path else {}
    )
    filesystem_manager.get_file_path_to_map.return_value = 'map'
    filesystem_manager.get_file_path_to_regions_template_file.return_value = 'regions_template'

    # Instantiate MapManager
    map_manager = MapManager('playthrough_name', filesystem_manager)
    map_manager.PlaceType = PlaceType

    # Call the method
    result = map_manager.get_place_full_data('region1')

    # Expected result
    expected_result = {
        'location_data': None,
        'area_data': None,
        'region_data': {
            'name': 'kingdom',
            'description': 'A vast kingdom'
        }
    }

    assert result == expected_result


def test_get_place_full_data_empty_identifier():
    filesystem_manager = Mock()
    map_manager = MapManager('playthrough_name', filesystem_manager)
    map_manager.PlaceType = PlaceType

    with pytest.raises(ValueError) as excinfo:
        map_manager.get_place_full_data('')

    assert str(excinfo.value) == "place_identifier should not be empty."


def test_get_place_full_data_nonexistent_identifier():
    # Mock FilesystemManager
    filesystem_manager = Mock()
    map_file = {}

    # Mock methods
    filesystem_manager.load_existing_or_new_json_file.return_value = map_file
    filesystem_manager.get_file_path_to_map.return_value = 'map'

    # Instantiate MapManager
    map_manager = MapManager('playthrough_name', filesystem_manager)
    map_manager.PlaceType = PlaceType

    with pytest.raises(ValueError) as excinfo:
        map_manager.get_place_full_data('unknown_place')

    assert str(excinfo.value) == "Place ID unknown_place not found."


def test_get_place_full_data_unknown_place_type():
    # Mock FilesystemManager
    filesystem_manager = Mock()

    # Sample data with unknown type
    map_file = {
        'place1': {
            'type': 'unknown_type',
            'place_template': 'some_template'
        }
    }

    # Mock methods
    filesystem_manager.load_existing_or_new_json_file.return_value = map_file
    filesystem_manager.get_file_path_to_map.return_value = 'map'

    # Instantiate MapManager
    map_manager = MapManager('playthrough_name', filesystem_manager)
    map_manager.PlaceType = PlaceType

    with pytest.raises(ValueError) as excinfo:
        map_manager.get_place_full_data('place1')

    assert str(excinfo.value) == "Unknown place type 'unknown_type' for place ID place1."


def test_get_place_full_data_missing_area_reference():
    # Mock FilesystemManager
    filesystem_manager = Mock()

    # Sample data with missing 'area' reference
    map_file = {
        'loc1': {
            'type': 'location',
            'place_template': 'cave'
            # 'area' key is missing
        }
    }
    location_templates = {
        'cave': {
            'description': 'A dark cave'
        }
    }

    # Mock methods
    filesystem_manager.load_existing_or_new_json_file.side_effect = lambda path: (
        map_file if 'map' in path else
        location_templates if 'locations_template' in path else {}
    )
    filesystem_manager.get_file_path_to_map.return_value = 'map'
    filesystem_manager.get_file_path_to_locations_template_file.return_value = 'locations_template'

    # Instantiate MapManager
    map_manager = MapManager('playthrough_name', filesystem_manager)
    map_manager.PlaceType = PlaceType

    with pytest.raises(ValueError) as excinfo:
        map_manager.get_place_full_data('loc1')

    assert str(excinfo.value) == "Area ID not found for location loc1."


def test_get_place_full_data_missing_template():
    # Mock FilesystemManager
    filesystem_manager = Mock()

    # Sample data
    map_file = {
        'region1': {
            'type': 'region',
            'place_template': 'unknown_template'
        }
    }
    region_templates = {
        # 'unknown_template' is missing
    }

    # Mock methods
    filesystem_manager.load_existing_or_new_json_file.side_effect = lambda path: (
        map_file if 'map' in path else
        region_templates if 'regions_template' in path else {}
    )
    filesystem_manager.get_file_path_to_map.return_value = 'map'
    filesystem_manager.get_file_path_to_regions_template_file.return_value = 'regions_template'

    # Instantiate MapManager
    map_manager = MapManager('playthrough_name', filesystem_manager)
    map_manager.PlaceType = PlaceType

    with pytest.raises(ValueError) as excinfo:
        map_manager.get_place_full_data('region1')

    assert str(excinfo.value) == "Region template 'unknown_template' not found."
