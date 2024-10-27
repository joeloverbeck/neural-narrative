# test_character_guidelines_manager.py

from unittest.mock import patch, call

import pytest

from src.characters.character_guidelines_manager import CharacterGuidelinesManager


# Assume the following imports based on the provided code structure

# Fixtures for mocking dependencies


@pytest.fixture
def mock_path_manager():
    with patch(
        "src.characters.character_guidelines_manager.PathManager"
    ) as MockPathManager:
        instance = MockPathManager.return_value
        instance.get_character_generation_guidelines_path.return_value = (
            "/mock/path/guidelines.json"
        )
        yield instance


@pytest.fixture
def mock_read_json_file():
    with patch(
        "src.characters.character_guidelines_manager.read_json_file"
    ) as mock_read:
        yield mock_read


@pytest.fixture
def mock_write_json_file():
    with patch(
        "src.characters.character_guidelines_manager.write_json_file"
    ) as mock_write:
        yield mock_write


@pytest.fixture
def mock_validate_non_empty_string():
    with patch(
        "src.characters.character_guidelines_manager.validate_non_empty_string"
    ) as mock_validate:
        yield mock_validate


# Test Initialization


def test_initialization_with_custom_path_manager(
    mock_path_manager, mock_read_json_file
):
    mock_read_json_file.return_value = {"universe:world:region:area": ["Guideline 1"]}

    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    mock_path_manager.get_character_generation_guidelines_path.assert_called_once()
    mock_read_json_file.assert_called_once_with("/mock/path/guidelines.json")
    assert manager._guidelines_file == {"universe:world:region:area": ["Guideline 1"]}


def test_initialization_with_default_path_manager(mock_read_json_file):
    with patch(
        "src.characters.character_guidelines_manager.PathManager"
    ) as MockPathManager:
        instance = MockPathManager.return_value
        instance.get_character_generation_guidelines_path.return_value = (
            "/default/path/guidelines.json"
        )
        mock_read_json_file.return_value = {
            "universe:world:region:area": ["Guideline 1"]
        }

        manager = CharacterGuidelinesManager()

        MockPathManager.assert_called_once()
        instance.get_character_generation_guidelines_path.assert_called_once()
        mock_read_json_file.assert_called_once_with("/default/path/guidelines.json")
        assert manager._guidelines_file == {
            "universe:world:region:area": ["Guideline 1"]
        }


# Test create_key


def test_create_key_with_location():
    key = CharacterGuidelinesManager.create_key(
        story_universe="UniverseA",
        world="WorldB",
        region="RegionC",
        area="AreaD",
        location="LocationE",
    )
    assert key == "UniverseA:WorldB:RegionC:AreaD:LocationE"


def test_create_key_without_location():
    key = CharacterGuidelinesManager.create_key(
        story_universe="UniverseA", world="WorldB", region="RegionC", area="AreaD"
    )
    assert key == "UniverseA:WorldB:RegionC:AreaD"


# Test load_guidelines


def test_load_guidelines_existing_key(mock_path_manager, mock_read_json_file):
    mock_read_json_file.return_value = {
        "UniverseA:WorldB:RegionC:AreaD:LocationE": ["Guideline 1", "Guideline 2"]
    }
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    guidelines = manager.load_guidelines(
        story_universe="UniverseA",
        world="WorldB",
        region="RegionC",
        area="AreaD",
        location="LocationE",
    )

    assert guidelines == ["Guideline 1", "Guideline 2"]


def test_load_guidelines_non_existing_key(mock_path_manager, mock_read_json_file):
    mock_read_json_file.return_value = {}
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    with pytest.raises(ValueError) as exc_info:
        manager.load_guidelines(
            story_universe="UniverseA",
            world="WorldB",
            region="RegionC",
            area="AreaD",
            location="LocationE",
        )

    assert (
        "No guidelines found for key 'UniverseA:WorldB:RegionC:AreaD:LocationE'."
        in str(exc_info.value)
    )


# Test save_guidelines


def test_save_guidelines_new_key(
    mock_path_manager,
    mock_read_json_file,
    mock_write_json_file,
    mock_validate_non_empty_string,
):
    mock_read_json_file.return_value = {}
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    guidelines = ["Guideline 1", "Guideline 2"]
    manager.save_guidelines(
        story_universe="UniverseA",
        world="WorldB",
        region="RegionC",
        area="AreaD",
        guidelines=guidelines,
        location="LocationE",
    )

    # Validate that each guideline was validated
    expected_calls = [
        call("Guideline 1", "guideline"),
        call("Guideline 2", "guideline"),
    ]
    mock_validate_non_empty_string.assert_has_calls(expected_calls, any_order=False)

    # Check that the new key was added
    assert manager._guidelines_file == {
        "UniverseA:WorldB:RegionC:AreaD:LocationE": ["Guideline 1", "Guideline 2"]
    }

    # Check that write_json_file was called with updated guidelines
    mock_write_json_file.assert_called_once_with(
        "/mock/path/guidelines.json",
        {"UniverseA:WorldB:RegionC:AreaD:LocationE": ["Guideline 1", "Guideline 2"]},
    )


def test_save_guidelines_existing_key(
    mock_path_manager,
    mock_read_json_file,
    mock_write_json_file,
    mock_validate_non_empty_string,
):
    mock_read_json_file.return_value = {
        "UniverseA:WorldB:RegionC:AreaD:LocationE": ["Guideline 1"]
    }
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    new_guidelines = ["Guideline 2", "Guideline 3"]
    manager.save_guidelines(
        story_universe="UniverseA",
        world="WorldB",
        region="RegionC",
        area="AreaD",
        guidelines=new_guidelines,
        location="LocationE",
    )

    # Validate that each new guideline was validated
    expected_calls = [
        call("Guideline 2", "guideline"),
        call("Guideline 3", "guideline"),
    ]
    mock_validate_non_empty_string.assert_has_calls(expected_calls, any_order=False)

    # Check that the guidelines were appended
    assert manager._guidelines_file == {
        "UniverseA:WorldB:RegionC:AreaD:LocationE": [
            "Guideline 1",
            "Guideline 2",
            "Guideline 3",
        ]
    }

    # Check that write_json_file was called with updated guidelines
    mock_write_json_file.assert_called_once_with(
        "/mock/path/guidelines.json",
        {
            "UniverseA:WorldB:RegionC:AreaD:LocationE": [
                "Guideline 1",
                "Guideline 2",
                "Guideline 3",
            ]
        },
    )


def test_save_guidelines_invalid_guidelines(
    mock_path_manager,
    mock_read_json_file,
    mock_write_json_file,
    mock_validate_non_empty_string,
):
    mock_read_json_file.return_value = {}
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    guidelines = ["Valid Guideline", ""]  # Second guideline is invalid

    # Configure validate_non_empty_string to raise ValueError for empty strings
    def validate_side_effect(value, field_name):
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")

    mock_validate_non_empty_string.side_effect = validate_side_effect

    with pytest.raises(ValueError) as exc_info:
        manager.save_guidelines(
            story_universe="UniverseA",
            world="WorldB",
            region="RegionC",
            area="AreaD",
            guidelines=guidelines,
            location="LocationE",
        )

    assert "guideline cannot be empty." in str(exc_info.value)

    # Ensure that write_json_file was never called due to validation failure
    mock_write_json_file.assert_not_called()


# Test guidelines_exist


def test_guidelines_exist_true(mock_path_manager, mock_read_json_file):
    mock_read_json_file.return_value = {
        "UniverseA:WorldB:RegionC:AreaD": ["Guideline 1"]
    }
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    exists = manager.guidelines_exist(
        story_universe="UniverseA", world="WorldB", region="RegionC", area="AreaD"
    )

    assert exists is True


def test_guidelines_exist_false(mock_path_manager, mock_read_json_file):
    mock_read_json_file.return_value = {}
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    exists = manager.guidelines_exist(
        story_universe="UniverseA", world="WorldB", region="RegionC", area="AreaD"
    )

    assert exists is False


# Test edge cases


def test_load_guidelines_empty_guidelines_file(mock_path_manager, mock_read_json_file):
    mock_read_json_file.return_value = {}
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    with pytest.raises(ValueError):
        manager.load_guidelines(
            story_universe="UniverseA", world="WorldB", region="RegionC", area="AreaD"
        )


def test_save_guidelines_empty_guidelines_list(
    mock_path_manager,
    mock_read_json_file,
    mock_write_json_file,
    mock_validate_non_empty_string,
):
    mock_read_json_file.return_value = {}
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    guidelines = []

    manager.save_guidelines(
        story_universe="UniverseA",
        world="WorldB",
        region="RegionC",
        area="AreaD",
        guidelines=guidelines,
    )

    # Since the guidelines list is empty, no validation should occur
    mock_validate_non_empty_string.assert_not_called()

    # Check that the key is added with an empty list
    assert manager._guidelines_file == {"UniverseA:WorldB:RegionC:AreaD": []}

    # Check that write_json_file was called with updated guidelines
    mock_write_json_file.assert_called_once_with(
        "/mock/path/guidelines.json", {"UniverseA:WorldB:RegionC:AreaD": []}
    )


def test_save_guidelines_duplicate_guidelines(
    mock_path_manager,
    mock_read_json_file,
    mock_write_json_file,
    mock_validate_non_empty_string,
):
    mock_read_json_file.return_value = {
        "UniverseA:WorldB:RegionC:AreaD": ["Guideline 1"]
    }
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    duplicate_guidelines = ["Guideline 1", "Guideline 2"]
    manager.save_guidelines(
        story_universe="UniverseA",
        world="WorldB",
        region="RegionC",
        area="AreaD",
        guidelines=duplicate_guidelines,
    )

    # Validate that each guideline was validated
    expected_calls = [
        call("Guideline 1", "guideline"),
        call("Guideline 2", "guideline"),
    ]
    mock_validate_non_empty_string.assert_has_calls(expected_calls, any_order=False)

    # Check that the guidelines were appended, including duplicates
    assert manager._guidelines_file == {
        "UniverseA:WorldB:RegionC:AreaD": ["Guideline 1", "Guideline 1", "Guideline 2"]
    }

    # Check that write_json_file was called with updated guidelines
    mock_write_json_file.assert_called_once_with(
        "/mock/path/guidelines.json",
        {
            "UniverseA:WorldB:RegionC:AreaD": [
                "Guideline 1",
                "Guideline 1",
                "Guideline 2",
            ]
        },
    )


# Test that _save_guidelines_file is called appropriately


def test_save_guidelines_calls_save_guidelines_file(
    mock_path_manager,
    mock_read_json_file,
    mock_write_json_file,
    mock_validate_non_empty_string,
):
    mock_read_json_file.return_value = {}
    manager = CharacterGuidelinesManager(path_manager=mock_path_manager)

    with patch.object(manager, "_save_guidelines_file") as mock_save:
        manager.save_guidelines(
            story_universe="UniverseA",
            world="WorldB",
            region="RegionC",
            area="AreaD",
            guidelines=["Guideline 1"],
        )
        mock_save.assert_called_once()
