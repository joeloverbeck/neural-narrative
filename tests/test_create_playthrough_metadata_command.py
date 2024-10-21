from unittest.mock import Mock, patch

import pytest

from src.base.commands.create_playthrough_metadata_command import (
    CreatePlaythroughMetadataCommand,
)
from src.base.constants import (
    STORY_UNIVERSES_TEMPLATE_FILE,
    DEFAULT_PLAYER_IDENTIFIER,
    DEFAULT_CURRENT_PLACE,
    DEFAULT_IDENTIFIER,
)
from src.base.exceptions import (
    PlaythroughAlreadyExistsError,
    StoryUniverseTemplateNotFoundError,
)
from src.base.required_string import RequiredString
from src.filesystem.filesystem_manager import FilesystemManager


def test_create_playthrough_success():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    story_universe_template = RequiredString("test_template")

    # Mock FilesystemManager with appropriate methods
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.playthrough_exists.return_value = False
    filesystem_manager.load_existing_or_new_json_file.return_value = {
        "test_template": {}
    }
    filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "metadata.json"
    )
    filesystem_manager.get_file_path_to_map.return_value = "map.json"
    filesystem_manager.get_file_path_to_playthrough_folder.return_value = (
        "/path/to/playthrough"
    )

    # Mock random.randint to return a fixed value
    with patch("random.randint", return_value=12):
        # Mock logger
        with patch("logging.getLogger") as mock_logger_get:
            mock_logger = Mock()
            mock_logger_get.return_value = mock_logger

            # Act
            command = CreatePlaythroughMetadataCommand(
                playthrough_name=playthrough_name,
                story_universe_template=story_universe_template,
                filesystem_manager=filesystem_manager,
            )

            command.execute()

            # Assert
            filesystem_manager.playthrough_exists.assert_called_once_with(
                "test_playthrough"
            )
            filesystem_manager.load_existing_or_new_json_file.assert_called_once_with(
                STORY_UNIVERSES_TEMPLATE_FILE
            )
            filesystem_manager.create_playthrough_folder.assert_called_once_with(
                RequiredString("test_playthrough")
            )
            filesystem_manager.get_file_path_to_playthrough_metadata.assert_called_once_with(
                RequiredString("test_playthrough")
            )
            expected_metadata = {
                "story_universe_template": "test_template",
                "player_identifier": DEFAULT_PLAYER_IDENTIFIER,
                "current_place": DEFAULT_CURRENT_PLACE,
                "time": {"hour": 12},
                "last_identifiers": {
                    "places": DEFAULT_IDENTIFIER,
                    "characters": DEFAULT_IDENTIFIER,
                },
                "followers": [],
            }
            filesystem_manager.save_json_file.assert_any_call(
                expected_metadata, "metadata.json"
            )
            filesystem_manager.get_file_path_to_map.assert_called_once_with(
                RequiredString("test_playthrough")
            )
            filesystem_manager.save_json_file.assert_any_call({}, "map.json")
            filesystem_manager.get_file_path_to_playthrough_folder.assert_called_once_with(
                RequiredString("test_playthrough")
            )


def test_create_playthrough_already_exists():
    # Arrange
    playthrough_name = RequiredString("existing_playthrough")
    story_universe_template = RequiredString("test_template")
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.playthrough_exists.return_value = True

    command = CreatePlaythroughMetadataCommand(
        playthrough_name=playthrough_name,
        story_universe_template=story_universe_template,
        filesystem_manager=filesystem_manager,
    )

    # Act and Assert
    with pytest.raises(PlaythroughAlreadyExistsError) as exc_info:
        command.execute()

    assert (
        str(exc_info.value)
        == f"A playthrough with the name '{playthrough_name}' already exists."
    )
    filesystem_manager.playthrough_exists.assert_called_once_with(
        "existing_playthrough"
    )
    assert filesystem_manager.create_playthrough_folder.call_count == 0


def test_story_universe_template_not_found():
    # Arrange
    playthrough_name = RequiredString("new_playthrough")
    story_universe_template = RequiredString("missing_template")
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.playthrough_exists.return_value = False
    filesystem_manager.load_existing_or_new_json_file.return_value = {
        "other_template": {}
    }

    command = CreatePlaythroughMetadataCommand(
        playthrough_name=playthrough_name,
        story_universe_template=story_universe_template,
        filesystem_manager=filesystem_manager,
    )

    # Act and Assert
    with pytest.raises(StoryUniverseTemplateNotFoundError) as exc_info:
        command.execute()

    assert (
        str(exc_info.value)
        == f"There is no such story universe template '{story_universe_template}'."
    )
    filesystem_manager.playthrough_exists.assert_called_once_with("new_playthrough")
    filesystem_manager.load_existing_or_new_json_file.assert_called_once_with(
        STORY_UNIVERSES_TEMPLATE_FILE
    )
    assert filesystem_manager.create_playthrough_folder.call_count == 0


def test_io_error_during_save():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    story_universe_template = RequiredString("test_template")
    filesystem_manager = Mock(spec=FilesystemManager)

    filesystem_manager.playthrough_exists.return_value = False
    filesystem_manager.load_existing_or_new_json_file.return_value = {
        "test_template": {}
    }
    filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "metadata.json"
    )
    filesystem_manager.get_file_path_to_map.return_value = "map.json"

    def save_json_file_side_effect(*args, **kwargs):
        raise IOError("Disk full")

    filesystem_manager.save_json_file.side_effect = save_json_file_side_effect

    with patch("logging.getLogger") as mock_logger_get:
        mock_logger = Mock()
        mock_logger_get.return_value = mock_logger

        command = CreatePlaythroughMetadataCommand(
            playthrough_name=playthrough_name,
            story_universe_template=story_universe_template,
            filesystem_manager=filesystem_manager,
        )

        with pytest.raises(IOError) as exc_info:
            command.execute()

        assert str(exc_info.value) == "Disk full"


def test_required_string_empty():
    with pytest.raises(ValueError) as exc_info:
        RequiredString("")

    assert str(exc_info.value) == "value can't be empty."


def test_required_string_none():
    with pytest.raises(ValueError) as exc_info:
        RequiredString(None)

    assert str(exc_info.value) == "value can't be empty."


def test_required_string_valid():
    s = RequiredString("valid_string")
    assert s.value == "valid_string"


def test_random_hour_is_within_range():
    playthrough_name = RequiredString("test_playthrough")
    story_universe_template = RequiredString("test_template")
    filesystem_manager = Mock(spec=FilesystemManager)

    filesystem_manager.playthrough_exists.return_value = False
    filesystem_manager.load_existing_or_new_json_file.return_value = {
        "test_template": {}
    }
    filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "metadata.json"
    )
    filesystem_manager.get_file_path_to_map.return_value = "map.json"
    filesystem_manager.get_file_path_to_playthrough_folder.return_value = (
        "/path/to/playthrough"
    )

    with patch("random.randint") as mock_randint:
        for hour in range(24):
            mock_randint.return_value = hour

            command = CreatePlaythroughMetadataCommand(
                playthrough_name=playthrough_name,
                story_universe_template=story_universe_template,
                filesystem_manager=filesystem_manager,
            )

            command.execute()

            metadata_saved_calls = filesystem_manager.save_json_file.call_args_list
            for call in metadata_saved_calls:
                args, kwargs = call
                data_saved = args[0]
                if "time" in data_saved:
                    assert data_saved["time"]["hour"] == hour
                    break
            filesystem_manager.save_json_file.reset_mock()


def test_required_string_from_required_string():
    s1 = RequiredString("value")
    s2 = RequiredString(s1)
    assert s2.value == "value"


def test_required_string_equality():
    s1 = RequiredString("value")
    s2 = RequiredString("value")
    s3 = RequiredString("other_value")

    assert s1 == s2
    assert s1 != s3


def test_required_string_comparison():
    s1 = RequiredString("abc")
    s2 = RequiredString("xyz")

    assert s1 < s2
    assert s2 > s1


def test_required_string_str_repr():
    s = RequiredString("value")
    assert str(s) == "value"
    assert repr(s) == "RequiredString(value='value')"
