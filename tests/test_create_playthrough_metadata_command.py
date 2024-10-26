from pathlib import Path
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
from src.filesystem.filesystem_manager import FilesystemManager


@patch("src.base.commands.create_playthrough_metadata_command.read_json_file")
def test_create_playthrough_success(mock_read_json_file):
    playthrough_name = "test_playthrough"
    story_universe_template = "test_template"
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.playthrough_exists.return_value = False
    mock_read_json_file.return_value = {"test_template": {}}
    (filesystem_manager.get_file_path_to_playthrough_metadata.return_value) = (
        "metadata.json"
    )
    filesystem_manager.get_file_path_to_map.return_value = "map.json"
    filesystem_manager.get_file_path_to_playthrough_folder.return_value = (
        "/path/to/playthrough"
    )
    with patch("random.randint", return_value=12):
        with patch("logging.getLogger") as mock_logger_get:
            mock_logger = Mock()
            mock_logger_get.return_value = mock_logger
            command = CreatePlaythroughMetadataCommand(
                playthrough_name=playthrough_name,
                story_universe_template=story_universe_template,
                filesystem_manager=filesystem_manager,
            )
            command.execute()
            filesystem_manager.playthrough_exists.assert_called_once_with(
                "test_playthrough"
            )
            mock_read_json_file(Path(STORY_UNIVERSES_TEMPLATE_FILE))
            filesystem_manager.create_playthrough_folder.assert_called_once_with(
                "test_playthrough"
            )
            filesystem_manager.get_file_path_to_playthrough_metadata.assert_called_once_with(
                "test_playthrough"
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
                "test_playthrough"
            )
            filesystem_manager.save_json_file.assert_any_call({}, "map.json")
            filesystem_manager.get_file_path_to_playthrough_folder.assert_called_once_with(
                "test_playthrough"
            )


def test_create_playthrough_already_exists():
    playthrough_name = "existing_playthrough"
    story_universe_template = "test_template"
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.playthrough_exists.return_value = True
    command = CreatePlaythroughMetadataCommand(
        playthrough_name=playthrough_name,
        story_universe_template=story_universe_template,
        filesystem_manager=filesystem_manager,
    )
    with pytest.raises(PlaythroughAlreadyExistsError) as exc_info:
        command.execute()
    assert f"A playthrough with the name '{playthrough_name}' already exists." in str(
        exc_info
    )
    filesystem_manager.playthrough_exists.assert_called_once_with(
        "existing_playthrough"
    )
    assert filesystem_manager.create_playthrough_folder.call_count == 0


@patch("src.base.commands.create_playthrough_metadata_command.read_json_file")
def test_story_universe_template_not_found(mock_read_json_file):
    playthrough_name = "new_playthrough"
    story_universe_template = "missing_template"
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.playthrough_exists.return_value = False
    mock_read_json_file.return_value = {"other_template": {}}
    command = CreatePlaythroughMetadataCommand(
        playthrough_name=playthrough_name,
        story_universe_template=story_universe_template,
        filesystem_manager=filesystem_manager,
    )
    with pytest.raises(StoryUniverseTemplateNotFoundError) as exc_info:
        command.execute()
    assert (
        f"There is no such story universe template '{story_universe_template}'."
        in str(exc_info)
    )
    filesystem_manager.playthrough_exists.assert_called_once_with("new_playthrough")
    mock_read_json_file.assert_called_once_with(Path(STORY_UNIVERSES_TEMPLATE_FILE))
    assert filesystem_manager.create_playthrough_folder.call_count == 0


@patch("src.base.commands.create_playthrough_metadata_command.read_json_file")
def test_io_error_during_save(mock_read_json_file):
    playthrough_name = "test_playthrough"
    story_universe_template = "test_template"
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.playthrough_exists.return_value = False
    mock_read_json_file.return_value = {"test_template": {}}
    (filesystem_manager.get_file_path_to_playthrough_metadata.return_value) = (
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
        assert "Disk full" in str(exc_info)


@patch("src.base.commands.create_playthrough_metadata_command.read_json_file")
def test_random_hour_is_within_range(mock_read_json_file):
    playthrough_name = "test_playthrough"
    story_universe_template = "test_template"
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.playthrough_exists.return_value = False
    mock_read_json_file.return_value = {"test_template": {}}
    (filesystem_manager.get_file_path_to_playthrough_metadata.return_value) = (
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
