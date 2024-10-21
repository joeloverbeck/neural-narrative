from typing import cast

import pytest

from src.base.required_string import RequiredString
from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.filesystem.filesystem_manager import FilesystemManager

# Mock constants and dependencies
CHARACTER_GENERATION_GUIDELINES_FILE = "character_guidelines.json"


# Mock FilesystemManager
class MockFilesystemManager:
    def __init__(self):
        # Simulate a JSON file with a dictionary
        self.files = {}

    def load_existing_or_new_json_file(self, file_name):
        return self.files.get(file_name.value, {})

    def save_json_file(self, data, file_name):
        self.files[file_name.value] = data


# Begin writing the tests


@pytest.fixture
def mock_filesystem_manager():
    return MockFilesystemManager()


@pytest.fixture
def manager(mock_filesystem_manager):
    return CharacterGuidelinesManager(
        filesystem_manager=cast(FilesystemManager, mock_filesystem_manager)
    )


def test_create_key_without_location():
    key = CharacterGuidelinesManager.create_key(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Europe"),
        RequiredString("France"),
    )
    assert key.value == "Universe:Earth:Europe:France"


def test_create_key_with_location():
    key = CharacterGuidelinesManager.create_key(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Europe"),
        RequiredString("France"),
        RequiredString("Paris"),
    )
    assert key.value == "Universe:Earth:Europe:France:Paris"


def test_save_and_load_guidelines(manager):
    # Prepare test data
    guidelines = [RequiredString("Be brave"), RequiredString("Be smart")]
    # Save guidelines
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Europe"),
        RequiredString("France"),
        guidelines,
        location=RequiredString("Paris"),
    )
    # Load guidelines
    loaded_guidelines = manager.load_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Europe"),
        RequiredString("France"),
        location=RequiredString("Paris"),
    )
    assert loaded_guidelines == guidelines


def test_guidelines_exist(manager):
    guidelines = [RequiredString("Be brave")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Asia"),
        RequiredString("Japan"),
        guidelines,
    )
    exists = manager.guidelines_exist(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Asia"),
        RequiredString("Japan"),
    )
    assert exists is True


def test_guidelines_not_exist(manager):
    exists = manager.guidelines_exist(
        RequiredString("Universe"),
        RequiredString("Mars"),
        RequiredString("Olympus Mons"),
        RequiredString("Base Camp"),
    )
    assert exists is False


def test_load_guidelines_nonexistent_key(manager):
    with pytest.raises(ValueError) as exc_info:
        manager.load_guidelines(
            RequiredString("Universe"),
            RequiredString("Mars"),
            RequiredString("Olympus Mons"),
            RequiredString("Base Camp"),
        )
    assert "No guidelines found for key 'Universe:Mars:Olympus Mons:Base Camp'." in str(
        exc_info.value
    )


def test_save_guidelines_append(manager):
    # First, save some guidelines
    initial_guidelines = [RequiredString("Be cautious")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Africa"),
        RequiredString("Egypt"),
        initial_guidelines,
    )
    # Now, save additional guidelines to the same key
    additional_guidelines = [RequiredString("Respect the culture")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Africa"),
        RequiredString("Egypt"),
        additional_guidelines,
    )
    # Load guidelines and check they include both initial and additional
    loaded_guidelines = manager.load_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Africa"),
        RequiredString("Egypt"),
    )
    all_guidelines = initial_guidelines + additional_guidelines
    assert loaded_guidelines == all_guidelines


def test_init_with_filesystem_manager(mock_filesystem_manager):
    # Instantiate with a provided filesystem_manager
    manager = CharacterGuidelinesManager(
        filesystem_manager=cast(FilesystemManager, mock_filesystem_manager)
    )
    assert manager._filesystem_manager is mock_filesystem_manager


def test_required_string_empty():
    with pytest.raises(ValueError) as exc_info:
        RequiredString("")
    assert "value can't be empty." in str(exc_info.value)


def test_required_string_non_string():
    with pytest.raises(TypeError) as exc_info:
        RequiredString(123)
    assert "value must be a string" in str(exc_info.value)


def test_required_string_comparison():
    str1 = RequiredString("abc")
    str2 = RequiredString("def")
    assert str1 < str2
    assert str1 != str2
    assert str1 == RequiredString("abc")


def test_required_string_repr():
    str1 = RequiredString("test")
    assert repr(str1) == "RequiredString(value='test')"


def test_guidelines_exist_with_location(manager):
    guidelines = [RequiredString("Stay hidden")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Planet X"),
        RequiredString("Unknown Region"),
        RequiredString("Sector 7"),
        guidelines,
        location=RequiredString("Area 51"),
    )
    exists = manager.guidelines_exist(
        RequiredString("Universe"),
        RequiredString("Planet X"),
        RequiredString("Unknown Region"),
        RequiredString("Sector 7"),
        location=RequiredString("Area 51"),
    )
    assert exists is True


def test_guidelines_not_exist_different_location(manager):
    guidelines = [RequiredString("Stay hidden")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Planet X"),
        RequiredString("Unknown Region"),
        RequiredString("Sector 7"),
        guidelines,
        location=RequiredString("Area 51"),
    )
    # Check that guidelines do not exist for a different location
    exists = manager.guidelines_exist(
        RequiredString("Universe"),
        RequiredString("Planet X"),
        RequiredString("Unknown Region"),
        RequiredString("Sector 7"),
        location=RequiredString("Area 52"),
    )
    assert exists is False


def test_save_and_load_guidelines_without_location(manager):
    guidelines = [RequiredString("Explore the unknown")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Planet Y"),
        RequiredString("Mystery Region"),
        RequiredString("Sector 9"),
        guidelines,
    )
    loaded_guidelines = manager.load_guidelines(
        RequiredString("Universe"),
        RequiredString("Planet Y"),
        RequiredString("Mystery Region"),
        RequiredString("Sector 9"),
    )
    assert loaded_guidelines == guidelines


def test_guidelines_file_persistence(manager):
    # Save guidelines
    guidelines = [RequiredString("Rule 1"), RequiredString("Rule 2")]
    manager.save_guidelines(
        RequiredString("Game"),
        RequiredString("World"),
        RequiredString("Region"),
        RequiredString("Area"),
        guidelines,
    )
    # Simulate reloading the manager (e.g., restarting the application)
    new_manager = CharacterGuidelinesManager(
        filesystem_manager=manager._filesystem_manager
    )
    loaded_guidelines = new_manager.load_guidelines(
        RequiredString("Game"),
        RequiredString("World"),
        RequiredString("Region"),
        RequiredString("Area"),
    )
    assert loaded_guidelines == guidelines


def test_invalid_required_string_in_guidelines(manager):
    # Attempt to save a guideline with an empty RequiredString
    with pytest.raises(ValueError) as exc_info:
        manager.save_guidelines(
            RequiredString("Universe"),
            RequiredString("Earth"),
            RequiredString("Europe"),
            RequiredString("Germany"),
            [RequiredString("")],
        )
    assert "value can't be empty." in str(exc_info.value)


def test_save_guidelines_duplicate_entries(manager):
    guidelines = [RequiredString("Be kind"), RequiredString("Be kind")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Australia"),
        RequiredString("Sydney"),
        guidelines,
    )
    loaded_guidelines = manager.load_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("Australia"),
        RequiredString("Sydney"),
    )
    # Both entries should be present
    assert loaded_guidelines == guidelines


def test_save_guidelines_special_characters(manager):
    guidelines = [
        RequiredString("Don't panic!"),
        RequiredString("Keep calm & carry on."),
    ]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("UK"),
        RequiredString("London"),
        guidelines,
    )
    loaded_guidelines = manager.load_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("UK"),
        RequiredString("London"),
    )
    assert loaded_guidelines == guidelines


def test_create_key_with_special_characters():
    key = CharacterGuidelinesManager.create_key(
        RequiredString("Uni:verse"),
        RequiredString("Wor:ld"),
        RequiredString("Re:gion"),
        RequiredString("Ar:ea"),
    )
    assert key.value == "Uni:verse:Wor:ld:Re:gion:Ar:ea"


def test_guidelines_exist_case_sensitivity(manager):
    guidelines = [RequiredString("Mind the gap")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("UK"),
        RequiredString("London"),
        guidelines,
    )
    # Check with different case
    exists = manager.guidelines_exist(
        RequiredString("universe"),
        RequiredString("earth"),
        RequiredString("uk"),
        RequiredString("london"),
    )
    assert exists is False  # Assuming the keys are case-sensitive


def test_load_guidelines_case_sensitivity(manager):
    guidelines = [RequiredString("Mind the gap")]
    manager.save_guidelines(
        RequiredString("Universe"),
        RequiredString("Earth"),
        RequiredString("UK"),
        RequiredString("London"),
        guidelines,
    )
    with pytest.raises(ValueError):
        manager.load_guidelines(
            RequiredString("universe"),
            RequiredString("earth"),
            RequiredString("uk"),
            RequiredString("london"),
        )
