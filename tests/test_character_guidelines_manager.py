from unittest.mock import patch

import pytest

from src.characters.character_guidelines_manager import CharacterGuidelinesManager

# Mock constant
CHARACTER_GENERATION_GUIDELINES_FILE = (
    "data/guidelines/character_generation_guidelines.json"
)


@pytest.fixture
def mock_filesystem_manager():
    """Fixture to create a mock FilesystemManager."""
    with patch("src.filesystem.filesystem_manager.FilesystemManager") as MockFS:
        mock_fs_instance = MockFS.return_value
        # Mock the load_existing_or_new_json_file to return an empty dict by default
        mock_fs_instance.load_existing_or_new_json_file.return_value = {}
        yield mock_fs_instance


@pytest.fixture
def manager(mock_filesystem_manager):
    """Fixture to create a CharacterGuidelinesManager with a mocked FilesystemManager."""
    return CharacterGuidelinesManager(filesystem_manager=mock_filesystem_manager)


class TestCharacterGuidelinesManager:
    def test_init_loads_guidelines_file(self, mock_filesystem_manager):
        """Test that the constructor loads the guidelines file."""
        CharacterGuidelinesManager(filesystem_manager=mock_filesystem_manager)
        mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once_with(
            CHARACTER_GENERATION_GUIDELINES_FILE
        )

    @pytest.mark.parametrize(
        "world, region, area, location, expected_key",
        [
            ("Earth", "North", "Forest", None, "Earth:North:Forest"),
            ("Mars", "South", "Desert", "Oasis", "Mars:South:Desert:Oasis"),
            ("", "Region", "Area", None, ValueError),
            ("World", "", "Area", None, ValueError),
            ("World", "Region", "", None, ValueError),
        ],
    )
    def test_create_key(self, world, region, area, location, expected_key):
        """Test the create_key static method."""
        if expected_key == ValueError:
            with pytest.raises(
                ValueError, match="World, region, and area can't be empty."
            ):
                CharacterGuidelinesManager.create_key(world, region, area, location)
        else:
            key = CharacterGuidelinesManager.create_key(world, region, area, location)
            assert key == expected_key

    def test_load_guidelines_existing_key(self, manager, mock_filesystem_manager):
        """Test loading guidelines for an existing key."""
        # Setup
        key = "Earth:North:Forest"
        guidelines = ["Guideline1", "Guideline2"]
        manager._guidelines_file[key] = guidelines

        # Action
        result = manager.load_guidelines("Earth", "North", "Forest")

        # Assert
        assert result == guidelines

    def test_load_guidelines_with_location(self, manager, mock_filesystem_manager):
        """Test loading guidelines with location."""
        key = "Mars:South:Desert:Oasis"
        guidelines = ["GuidelineA", "GuidelineB"]
        manager._guidelines_file[key] = guidelines

        result = manager.load_guidelines("Mars", "South", "Desert", "Oasis")

        assert result == guidelines

    def test_load_guidelines_non_existing_key(self, manager):
        """Test loading guidelines for a non-existing key raises ValueError."""
        with pytest.raises(
            ValueError, match="No guidelines found for key 'Earth:East:Mountain'."
        ):
            manager.load_guidelines("Earth", "East", "Mountain")

    def test_save_guidelines(self, manager, mock_filesystem_manager):
        """Test saving guidelines updates the internal dictionary and calls save."""
        world, region, area, location = "Venus", "West", "Lake", "Dock"
        guidelines = ["NewGuideline1", "NewGuideline2"]

        manager.save_guidelines(world, region, area, guidelines, location)

        # Check if the internal dictionary was updated correctly
        expected_key = "Venus:West:Lake:Dock"
        assert manager._guidelines_file[expected_key] == guidelines

        # Check if save_json_file was called with correct parameters
        mock_filesystem_manager.save_json_file.assert_called_once_with(
            manager._guidelines_file,
            CHARACTER_GENERATION_GUIDELINES_FILE,
        )

    def test_save_guidelines_without_location(self, manager, mock_filesystem_manager):
        """Test saving guidelines without a location."""
        world, region, area = "Jupiter", "North", "Storm"
        guidelines = ["StormGuideline1"]

        manager.save_guidelines(world, region, area, guidelines)

        expected_key = "Jupiter:North:Storm"
        assert manager._guidelines_file[expected_key] == guidelines

        mock_filesystem_manager.save_json_file.assert_called_once_with(
            manager._guidelines_file,
            CHARACTER_GENERATION_GUIDELINES_FILE,
        )

    @pytest.mark.parametrize(
        "world, region, area, location, expected",
        [
            ("Earth", "North", "Forest", None, False),
            ("Mars", "South", "Desert", "Oasis", False),
            ("Venus", "West", "Lake", "Dock", True),
            ("Jupiter", "North", "Storm", None, True),
        ],
    )
    def test_guidelines_exist(
        self, manager, mock_filesystem_manager, world, region, area, location, expected
    ):
        """Test checking if guidelines exist for a given key."""
        if expected:
            key = CharacterGuidelinesManager.create_key(world, region, area, location)
            manager._guidelines_file[key] = ["Some guideline"]

        exists = manager.guidelines_exist(world, region, area, location)
        assert exists == expected

    def test_guidelines_exist_with_location(self, manager):
        """Test guidelines_exist method with location."""
        key_existing = "Saturn:East:Ring:Gateway"
        key_non_existing = "Saturn:West:Moon"

        manager._guidelines_file[key_existing] = ["GuidelineX"]

        assert manager.guidelines_exist("Saturn", "East", "Ring", "Gateway") is True
        assert manager.guidelines_exist("Saturn", "West", "Moon") is False

    def test_create_key_with_empty_world(self, manager):
        """Test create_key raises ValueError when world is empty."""
        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.create_key("", "Region", "Area")

    def test_create_key_with_empty_region(self, manager):
        """Test create_key raises ValueError when region is empty."""
        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.create_key("World", "", "Area")

    def test_create_key_with_empty_area(self, manager):
        """Test create_key raises ValueError when area is empty."""
        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.create_key("World", "Region", "")

    def test_init_with_default_filesystem_manager(self):
        """Test that CharacterGuidelinesManager initializes FilesystemManager when none is provided."""
        with patch(
            "src.characters.character_guidelines_manager.FilesystemManager"
        ) as MockFS:
            mock_fs_instance = MockFS.return_value
            mock_fs_instance.load_existing_or_new_json_file.return_value = {}
            manager = CharacterGuidelinesManager()
            MockFS.assert_called_once()
            mock_fs_instance.load_existing_or_new_json_file.assert_called_once_with(
                CHARACTER_GENERATION_GUIDELINES_FILE
            )

    def test_load_guidelines_with_empty_world_region_area(self, manager):
        """Test load_guidelines with empty world, region, or area raises ValueError."""
        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.load_guidelines("", "North", "Forest")

        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.load_guidelines("Earth", "", "Forest")

        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.load_guidelines("Earth", "North", "")

    def test_save_guidelines_with_empty_world_region_area(self, manager):
        """Test save_guidelines with empty world, region, or area raises ValueError."""
        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.save_guidelines("", "North", "Forest", ["Guideline1"])

        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.save_guidelines("Earth", "", "Forest", ["Guideline1"])

        with pytest.raises(ValueError, match="World, region, and area can't be empty."):
            manager.save_guidelines("Earth", "North", "", ["Guideline1"])

    def test_save_guidelines_overwrites_existing_guidelines(
        self, manager, mock_filesystem_manager
    ):
        """Test that saving guidelines overwrites existing ones."""
        key = "Earth:North:Forest"
        initial_guidelines = ["InitialGuideline"]
        updated_guidelines = ["UpdatedGuideline1", "UpdatedGuideline2"]
        manager._guidelines_file[key] = initial_guidelines

        manager.save_guidelines("Earth", "North", "Forest", updated_guidelines)

        assert manager._guidelines_file[key] == updated_guidelines
        mock_filesystem_manager.save_json_file.assert_called_once_with(
            manager._guidelines_file,
            CHARACTER_GENERATION_GUIDELINES_FILE,
        )

    def test_filesystem_manager_save_json_file_called_correctly(
        self, manager, mock_filesystem_manager
    ):
        """Test that _save_guidelines_file calls save_json_file with correct parameters."""
        manager._guidelines_file = {"Earth:North:Forest": ["Guideline1"]}
        manager._save_guidelines_file()
        mock_filesystem_manager.save_json_file.assert_called_once_with(
            manager._guidelines_file,
            CHARACTER_GENERATION_GUIDELINES_FILE,
        )

    def test_filesystem_manager_load_existing_or_new_json_file_called_once(
        self, mock_filesystem_manager
    ):
        """Test that FilesystemManager.load_existing_or_new_json_file is called once during initialization."""
        CharacterGuidelinesManager(filesystem_manager=mock_filesystem_manager)
        mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once_with(
            CHARACTER_GENERATION_GUIDELINES_FILE
        )
