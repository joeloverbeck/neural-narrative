from typing import cast

import pytest

from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.filesystem.filesystem_manager import FilesystemManager

CHARACTER_GENERATION_GUIDELINES_FILE = "character_guidelines.json"


class MockFilesystemManager:

    def __init__(self):
        self.files = {}

    def load_existing_or_new_json_file(self, file_name):
        return self.files.get(file_name, {})

    def save_json_file(self, data, file_name):
        self.files[file_name] = data


@pytest.fixture
def mock_filesystem_manager():
    return MockFilesystemManager()


@pytest.fixture
def manager(mock_filesystem_manager):
    return CharacterGuidelinesManager(
        filesystem_manager=cast(FilesystemManager, mock_filesystem_manager)
    )


def test_create_key_without_location():
    key = CharacterGuidelinesManager.create_key("Universe", "Earth", "Europe", "France")
    assert key == "Universe:Earth:Europe:France"


def test_create_key_with_location():
    key = CharacterGuidelinesManager.create_key(
        "Universe", "Earth", "Europe", "France", "Paris"
    )
    assert key == "Universe:Earth:Europe:France:Paris"


def test_save_and_load_guidelines(manager):
    guidelines = ["Be brave", "Be smart"]
    manager.save_guidelines(
        "Universe", "Earth", "Europe", "France", guidelines, location="Paris"
    )
    loaded_guidelines = manager.load_guidelines(
        "Universe", "Earth", "Europe", "France", location="Paris"
    )
    assert loaded_guidelines == guidelines


def test_guidelines_exist(manager):
    guidelines = ["Be brave"]
    manager.save_guidelines("Universe", "Earth", "Asia", "Japan", guidelines)
    exists = manager.guidelines_exist("Universe", "Earth", "Asia", "Japan")
    assert exists is True


def test_guidelines_not_exist(manager):
    exists = manager.guidelines_exist("Universe", "Mars", "Olympus Mons", "Base Camp")
    assert exists is False


def test_load_guidelines_nonexistent_key(manager):
    with pytest.raises(ValueError) as exc_info:
        manager.load_guidelines("Universe", "Mars", "Olympus Mons", "Base Camp")
    assert "No guidelines found for key 'Universe:Mars:Olympus Mons:Base Camp'." in str(
        exc_info
    )


def test_save_guidelines_append(manager):
    initial_guidelines = ["Be cautious"]
    manager.save_guidelines("Universe", "Earth", "Africa", "Egypt", initial_guidelines)
    additional_guidelines = ["Respect the culture"]
    manager.save_guidelines(
        "Universe", "Earth", "Africa", "Egypt", additional_guidelines
    )
    loaded_guidelines = manager.load_guidelines("Universe", "Earth", "Africa", "Egypt")
    all_guidelines = initial_guidelines + additional_guidelines
    assert loaded_guidelines == all_guidelines


def test_init_with_filesystem_manager(mock_filesystem_manager):
    manager = CharacterGuidelinesManager(
        filesystem_manager=cast(FilesystemManager, mock_filesystem_manager)
    )
    assert manager._filesystem_manager is mock_filesystem_manager


def test_guidelines_exist_with_location(manager):
    guidelines = ["Stay hidden"]
    manager.save_guidelines(
        "Universe",
        "Planet X",
        "Unknown Region",
        "Sector 7",
        guidelines,
        location="Area 51",
    )
    exists = manager.guidelines_exist(
        "Universe", "Planet X", "Unknown Region", "Sector 7", location="Area 51"
    )
    assert exists is True


def test_guidelines_not_exist_different_location(manager):
    guidelines = ["Stay hidden"]
    manager.save_guidelines(
        "Universe",
        "Planet X",
        "Unknown Region",
        "Sector 7",
        guidelines,
        location="Area 51",
    )
    exists = manager.guidelines_exist(
        "Universe", "Planet X", "Unknown Region", "Sector 7", location="Area 52"
    )
    assert exists is False


def test_save_and_load_guidelines_without_location(manager):
    guidelines = ["Explore the unknown"]
    manager.save_guidelines(
        "Universe", "Planet Y", "Mystery Region", "Sector 9", guidelines
    )
    loaded_guidelines = manager.load_guidelines(
        "Universe", "Planet Y", "Mystery Region", "Sector 9"
    )
    assert loaded_guidelines == guidelines


def test_guidelines_file_persistence(manager):
    guidelines = ["Rule 1", "Rule 2"]
    manager.save_guidelines("Game", "World", "Region", "Area", guidelines)
    new_manager = CharacterGuidelinesManager(
        filesystem_manager=manager._filesystem_manager
    )
    loaded_guidelines = new_manager.load_guidelines("Game", "World", "Region", "Area")
    assert loaded_guidelines == guidelines


def test_invalid_required_string_in_guidelines(manager):
    with pytest.raises(ValueError) as exc_info:
        manager.save_guidelines("Universe", "Earth", "Europe", "Germany", [""])
    assert "must be a non-empty string" in str(exc_info)


def test_save_guidelines_duplicate_entries(manager):
    guidelines = ["Be kind", "Be kind"]
    manager.save_guidelines("Universe", "Earth", "Australia", "Sydney", guidelines)
    loaded_guidelines = manager.load_guidelines(
        "Universe", "Earth", "Australia", "Sydney"
    )
    assert loaded_guidelines == guidelines


def test_save_guidelines_special_characters(manager):
    guidelines = ["Don't panic!", "Keep calm & carry on."]
    manager.save_guidelines("Universe", "Earth", "UK", "London", guidelines)
    loaded_guidelines = manager.load_guidelines("Universe", "Earth", "UK", "London")
    assert loaded_guidelines == guidelines


def test_create_key_with_special_characters():
    key = CharacterGuidelinesManager.create_key(
        "Uni:verse", "Wor:ld", "Re:gion", "Ar:ea"
    )
    assert key == "Uni:verse:Wor:ld:Re:gion:Ar:ea"


def test_guidelines_exist_case_sensitivity(manager):
    guidelines = ["Mind the gap"]
    manager.save_guidelines("Universe", "Earth", "UK", "London", guidelines)
    exists = manager.guidelines_exist("universe", "earth", "uk", "london")
    assert exists is False


def test_load_guidelines_case_sensitivity(manager):
    guidelines = ["Mind the gap"]
    manager.save_guidelines("Universe", "Earth", "UK", "London", guidelines)
    with pytest.raises(ValueError):
        manager.load_guidelines("universe", "earth", "uk", "london")
