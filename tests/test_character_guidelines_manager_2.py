# Sample data to be used in tests
from unittest.mock import patch, MagicMock

import pytest

from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.filesystem.path_manager import PathManager

MOCK_GUIDELINES_DATA = {
    "The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak": [
        "A 400-year-old celestial serpent, wise yet mischievous, with the ability to shapeshift into a human form. This ancient being has witnessed countless reincarnations on the sacred mountain and often acts as a guide to pilgrims seeking enlightenment. Despite their profound knowledge, they have a penchant for playing pranks on unsuspecting visitors, adding a touch of cosmic humor to their interactions.",
        "A 25-year-old human soul-weaver from Tokyo who can create art installations that combine physical materials with crystallized memories from past lives. Driven by a desire to help others find meaning in their reincarnated existences, they struggle with the weight of their own fragmented past lives. Their unique ability has brought them fame and success but also loneliness, as they grapple with the burden of too many memories.",
        "A 100-year-old ethereal herb grower who can communicate with the spirit-flowers of the floating gardens. This gentle being has honed their gardening skills over multiple lifetimes, cultivating rare herbs that grow only in the ephemeral spaces between worlds. They are known for their deep connection to nature and their willingness to share their knowledge with those who show reverence for the mountain's sacred ecosystem. However, they must navigate the challenges of preserving their mystical plants in a world increasingly dominated by technology and commerce.",
    ],
    # Add more keys if needed for other tests
}


@pytest.fixture
def mock_read_json_file():
    with patch(
        "src.characters.character_guidelines_manager.read_json_file"
    ) as mock_read:
        mock_read.return_value = MOCK_GUIDELINES_DATA
        yield mock_read


@pytest.fixture
def mock_write_json_file():
    with patch(
        "src.characters.character_guidelines_manager.write_json_file"
    ) as mock_write:
        yield mock_write


@pytest.fixture
def mock_path_manager():
    with patch(
        "src.characters.character_guidelines_manager.PathManager"
    ) as mock_pm_class:
        mock_pm_instance = MagicMock(spec=PathManager)
        # Assuming the method get_character_generation_guidelines_path returns a string path
        mock_pm_instance.get_character_generation_guidelines_path.return_value = (
            "/fake/path/guidelines.json"
        )
        mock_pm_class.return_value = mock_pm_instance
        yield mock_pm_instance


def test_load_guidelines_with_existing_key(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    manager = CharacterGuidelinesManager()

    story_universe = "The Whimsical Divine Playground"
    world = "Reincarnation Earth"
    region = "Shinwa-koku"
    area = "Celestial Garden Peak"
    location = None  # No location provided

    expected_guidelines = MOCK_GUIDELINES_DATA[
        "The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak"
    ]

    guidelines = manager.load_guidelines(
        story_universe=story_universe,
        world=world,
        region=region,
        area=area,
        location=location,
    )

    assert (
        guidelines == expected_guidelines
    ), "Guidelines do not match the expected data."


def test_load_guidelines_with_missing_key(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    manager = CharacterGuidelinesManager()

    story_universe = "Non-Existent Universe"
    world = "Unknown World"
    region = "Mystery Region"
    area = "Hidden Area"
    location = None  # No location provided

    with pytest.raises(ValueError) as exc_info:
        manager.load_guidelines(
            story_universe=story_universe,
            world=world,
            region=region,
            area=area,
            location=location,
        )

    assert (
        str(exc_info.value)
        == f"No guidelines found for key 'Non-Existent Universe:Unknown World:Mystery Region:Hidden Area'."
    ), "ValueError message does not match expected."


def test_load_guidelines_with_optional_location(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    # Add a key with location to the mock data
    mock_guidelines_data_with_location = {
        "The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak:Hidden Valley": [
            "Guideline 1 for Hidden Valley.",
            "Guideline 2 for Hidden Valley.",
        ]
    }

    with patch(
        "src.characters.character_guidelines_manager.read_json_file",
        return_value=mock_guidelines_data_with_location,
    ):
        manager = CharacterGuidelinesManager()

        story_universe = "The Whimsical Divine Playground"
        world = "Reincarnation Earth"
        region = "Shinwa-koku"
        area = "Celestial Garden Peak"
        location = "Hidden Valley"

        expected_guidelines = mock_guidelines_data_with_location[
            "The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak:Hidden Valley"
        ]

        guidelines = manager.load_guidelines(
            story_universe=story_universe,
            world=world,
            region=region,
            area=area,
            location=location,
        )

        assert (
            guidelines == expected_guidelines
        ), "Guidelines with location do not match expected data."


def test_load_guidelines_with_empty_guidelines(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    # Add a key with empty guidelines
    MOCK_GUIDELINES_DATA_EMPTY = {
        "Empty Universe:Empty World:Empty Region:Empty Area": []
    }

    with patch(
        "src.characters.character_guidelines_manager.read_json_file",
        return_value=MOCK_GUIDELINES_DATA_EMPTY,
    ):
        manager = CharacterGuidelinesManager()

        story_universe = "Empty Universe"
        world = "Empty World"
        region = "Empty Region"
        area = "Empty Area"
        location = None  # No location provided

        guidelines = manager.load_guidelines(
            story_universe=story_universe,
            world=world,
            region=region,
            area=area,
            location=location,
        )

        assert guidelines == [], "Guidelines should be an empty list."


def test_save_guidelines_creates_new_key(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    manager = CharacterGuidelinesManager()

    story_universe = "New Universe"
    world = "New World"
    region = "New Region"
    area = "New Area"
    location = None  # No location provided
    new_guidelines = ["New guideline 1.", "New guideline 2."]

    manager.save_guidelines(
        story_universe=story_universe,
        world=world,
        region=region,
        area=area,
        guidelines=new_guidelines,
        location=location,
    )

    expected_key = "New Universe:New World:New Region:New Area"
    expected_guidelines = new_guidelines

    # Verify that the key was added to the guidelines file
    assert (
        manager._guidelines_file[expected_key] == expected_guidelines
    ), "New key was not added correctly."

    # Verify that write_json_file was called with the updated guidelines
    mock_write_json_file.assert_called_once_with(
        "/fake/path/guidelines.json",
        manager._guidelines_file,
    )


def test_save_guidelines_appends_to_existing_key(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    manager = CharacterGuidelinesManager()

    story_universe = "The Whimsical Divine Playground"
    world = "Reincarnation Earth"
    region = "Shinwa-koku"
    area = "Celestial Garden Peak"
    location = None  # No location provided
    additional_guidelines = ["Additional guideline 1.", "Additional guideline 2."]

    initial_guidelines = MOCK_GUIDELINES_DATA[
        "The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak"
    ]

    manager.save_guidelines(
        story_universe=story_universe,
        world=world,
        region=region,
        area=area,
        guidelines=additional_guidelines,
        location=location,
    )

    expected_key = "The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak"

    expected_guidelines = []
    expected_guidelines.extend(initial_guidelines)

    # Verify that the guidelines were appended
    assert (
        manager._guidelines_file[expected_key] == expected_guidelines
    ), "Guidelines were not appended correctly."

    # Verify that write_json_file was called with the updated guidelines
    mock_write_json_file.assert_called_once_with(
        "/fake/path/guidelines.json",
        manager._guidelines_file,
    )


def test_guidelines_exist_returns_true(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    manager = CharacterGuidelinesManager()

    story_universe = "The Whimsical Divine Playground"
    world = "Reincarnation Earth"
    region = "Shinwa-koku"
    area = "Celestial Garden Peak"
    location = None  # No location provided

    exists = manager.guidelines_exist(
        story_universe=story_universe,
        world=world,
        region=region,
        area=area,
        location=location,
    )

    assert exists is True, "guidelines_exist should return True for existing key."


def test_guidelines_exist_returns_false(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    manager = CharacterGuidelinesManager()

    story_universe = "Non-Existent Universe"
    world = "Unknown World"
    region = "Mystery Region"
    area = "Hidden Area"
    location = None  # No location provided

    exists = manager.guidelines_exist(
        story_universe=story_universe,
        world=world,
        region=region,
        area=area,
        location=location,
    )

    assert exists is False, "guidelines_exist should return False for non-existing key."


def test_create_key_with_location():
    story_universe = "Universe"
    world = "World"
    region = "Region"
    area = "Area"
    location = "Location"

    expected_key = "Universe:World:Region:Area:Location"
    generated_key = CharacterGuidelinesManager.create_key(
        story_universe, world, region, area, location
    )

    assert (
        generated_key == expected_key
    ), "create_key did not generate the expected key with location."


def test_create_key_without_location():
    story_universe = "Universe"
    world = "World"
    region = "Region"
    area = "Area"
    location = None

    expected_key = "Universe:World:Region:Area"
    generated_key = CharacterGuidelinesManager.create_key(
        story_universe, world, region, area, location
    )

    assert (
        generated_key == expected_key
    ), "create_key did not generate the expected key without location."


def test_load_guidelines_trimmed_strings(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    # Add a key with leading/trailing spaces to the mock data
    key_with_spaces = " The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak "
    MOCK_GUIDELINES_DATA_SPACED = {
        key_with_spaces.strip(): MOCK_GUIDELINES_DATA[
            "The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak"
        ]
    }

    with patch(
        "src.characters.character_guidelines_manager.read_json_file",
        return_value=MOCK_GUIDELINES_DATA_SPACED,
    ):
        manager = CharacterGuidelinesManager()

        story_universe = "The Whimsical Divine Playground"
        world = "Reincarnation Earth"
        region = "Shinwa-koku"
        area = "Celestial Garden Peak"
        location = None  # No location provided

        expected_guidelines = MOCK_GUIDELINES_DATA[
            "The Whimsical Divine Playground:Reincarnation Earth:Shinwa-koku:Celestial Garden Peak"
        ]

        guidelines = manager.load_guidelines(
            story_universe=story_universe,
            world=world,
            region=region,
            area=area,
            location=location,
        )

        assert (
            guidelines == expected_guidelines
        ), "Guidelines do not match when keys have leading/trailing spaces."


def test_load_guidelines_case_sensitivity(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    manager = CharacterGuidelinesManager()

    # Attempt to load with different casing
    story_universe = "the whimsical divine playground"  # lowercase
    world = "reincarnation earth"  # lowercase
    region = "shinwa-koku"  # lowercase
    area = "celestial garden peak"  # lowercase
    location = None  # No location provided

    with pytest.raises(ValueError) as exc_info:
        manager.load_guidelines(
            story_universe=story_universe,
            world=world,
            region=region,
            area=area,
            location=location,
        )

    expected_key = "the whimsical divine playground:reincarnation earth:shinwa-koku:celestial garden peak"
    assert (
        str(exc_info.value) == f"No guidelines found for key '{expected_key}'."
    ), "ValueError message does not match expected for case sensitivity test."


def test_save_guidelines_with_invalid_guideline(
    mock_read_json_file, mock_write_json_file, mock_path_manager
):
    manager = CharacterGuidelinesManager()

    story_universe = "Universe"
    world = "World"
    region = "Region"
    area = "Area"
    location = None  # No location provided
    invalid_guidelines = ["Valid guideline.", ""]  # Second guideline is empty

    with pytest.raises(ValueError) as exc_info:
        manager.save_guidelines(
            story_universe=story_universe,
            world=world,
            region=region,
            area=area,
            guidelines=invalid_guidelines,
            location=location,
        )

    assert (
        str(exc_info.value) == "'guideline' must be a non-empty string."
    ), "ValueError message does not match expected for invalid guideline."
