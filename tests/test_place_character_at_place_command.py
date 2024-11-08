from unittest.mock import MagicMock, patch

import pytest

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.maps.map_repository import MapRepository
from src.movements.commands.place_character_at_place_command import (
    PlaceCharacterAtPlaceCommand,
)
from src.movements.exceptions import PlaceCharacterAtPlaceError


# Fixture for mocking PlaythroughManager
@pytest.fixture
def mock_playthrough_manager():
    mock = MagicMock(spec=PlaythroughManager)
    return mock


# Fixture for mocking MapRepository
@pytest.fixture
def mock_map_repository():
    mock = MagicMock(spec=MapRepository)
    return mock


# Helper function to create a valid map data structure
def create_valid_map_data(place_id, place_type, characters=None):
    return {place_id: {"type": place_type, "characters": characters or []}}


# Test initialization with valid inputs
def test_initialization_valid_inputs(mock_playthrough_manager, mock_map_repository):
    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    assert command._character_identifier == "Char1"
    assert command._place_identifier == "Place1"
    assert command._playthrough_manager == mock_playthrough_manager
    assert command._map_repository == mock_map_repository


# Test initialization without providing PlaythroughManager and MapRepository
@patch("src.movements.commands.place_character_at_place_command.PlaythroughManager")
@patch("src.movements.commands.place_character_at_place_command.MapRepository")
def test_initialization_defaults(mock_map_repo_class, mock_playthrough_manager_class):
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_map_repo = MagicMock(spec=MapRepository)

    mock_playthrough_manager_class.return_value = mock_playthrough_manager
    mock_map_repo_class.return_value = mock_map_repo

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
    )

    mock_playthrough_manager_class.assert_called_once_with("TestPlaythrough")
    mock_map_repo_class.assert_called_once_with("TestPlaythrough")
    assert command._playthrough_manager == mock_playthrough_manager
    assert command._map_repository == mock_map_repo


# Test initialization with empty playthrough_name
def test_initialization_empty_playthrough_name():
    with pytest.raises(ValueError):
        PlaceCharacterAtPlaceCommand(
            playthrough_name="", character_identifier="Char1", place_identifier="Place1"
        )


# Test initialization with empty character_identifier
def test_initialization_empty_character_identifier():
    with pytest.raises(ValueError):
        PlaceCharacterAtPlaceCommand(
            playthrough_name="TestPlaythrough",
            character_identifier="",
            place_identifier="Place1",
        )


# Test initialization with empty place_identifier
def test_initialization_empty_place_identifier():
    with pytest.raises(ValueError):
        PlaceCharacterAtPlaceCommand(
            playthrough_name="TestPlaythrough",
            character_identifier="Char1",
            place_identifier="",
        )


# Test execute raises error if character is a follower
def test_execute_character_is_follower(mock_playthrough_manager, mock_map_repository):
    mock_playthrough_manager.get_followers.return_value = ["Char1", "Char2"]

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(PlaceCharacterAtPlaceError) as exc_info:
        command.execute()

    assert "is one of the followers" in str(exc_info.value)
    mock_playthrough_manager.get_followers.assert_called_once()


# Test execute raises ValueError if place not found
def test_execute_place_not_found(mock_playthrough_manager, mock_map_repository):
    mock_playthrough_manager.get_followers.return_value = []
    mock_map_repository.load_map_data.return_value = {}

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="NonExistentPlace",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(ValueError) as exc_info:
        command.execute()

    assert "Place ID NonExistentPlace not found." in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Test execute raises error if place type cannot house characters
def test_execute_invalid_place_type(mock_playthrough_manager, mock_map_repository):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data("Place1", TemplateType.WORLD.value)
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(PlaceCharacterAtPlaceError) as exc_info:
        command.execute()

    assert "cannot house characters" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Test execute raises error if character is already at the place
def test_execute_character_already_at_place(
    mock_playthrough_manager, mock_map_repository
):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data(
        "Place1", TemplateType.ROOM.value, characters=["Char1", "Char2"]
    )
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(PlaceCharacterAtPlaceError) as exc_info:
        command.execute()

    assert "is already at place Place1" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Test execute successfully adds character to existing characters list
def test_execute_adds_character_successfully(
    mock_playthrough_manager, mock_map_repository
):
    mock_playthrough_manager.get_followers.return_value = []
    initial_characters = ["Char2", "Char3"]
    map_data = create_valid_map_data(
        "Place1", TemplateType.LOCATION.value, characters=initial_characters.copy()
    )
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with patch(
        "src.movements.commands.place_character_at_place_command.logger"
    ) as mock_logger:
        command.execute()

    assert "Char1" in map_data["Place1"]["characters"]
    mock_map_repository.save_map_data.assert_called_once_with(map_data)
    mock_logger.info.assert_called_once()
    logged_message = mock_logger.info.call_args[0][0]
    assert "placed at" in logged_message
    assert "Char1" in logged_message
    assert "Place1" in logged_message
    assert map_data["Place1"]["characters"] == initial_characters + ["Char1"]


# Test execute successfully adds character when 'characters' is None
def test_execute_adds_character_with_none_characters(
    mock_playthrough_manager, mock_map_repository
):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data("Place1", TemplateType.AREA.value, characters=None)
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with patch(
        "src.movements.commands.place_character_at_place_command.logger"
    ) as mock_logger:
        command.execute()

    assert map_data["Place1"]["characters"] == ["Char1"]
    mock_map_repository.save_map_data.assert_called_once_with(map_data)
    mock_logger.info.assert_called_once()


# Test execute successfully adds character when 'characters' key is missing
def test_execute_adds_character_with_missing_characters_key(
    mock_playthrough_manager, mock_map_repository
):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = {
        "Place1": {
            "type": TemplateType.ROOM.value
            # 'characters' key is missing
        }
    }
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with patch(
        "src.movements.commands.place_character_at_place_command.logger"
    ) as mock_logger:
        command.execute()

    assert map_data["Place1"]["characters"] == ["Char1"]
    mock_map_repository.save_map_data.assert_called_once_with(map_data)
    mock_logger.info.assert_called_once()


# Test execute logs the correct information
def test_execute_logging(mock_playthrough_manager, mock_map_repository):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data(
        "Place1", TemplateType.ROOM.value, characters=["Char2"]
    )
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with patch(
        "src.movements.commands.place_character_at_place_command.logger"
    ) as mock_logger:
        command.execute()

    expected_characters = ["Char2", "Char1"]
    mock_logger.info.assert_called_once_with(
        f"Character 'Char1' placed at room 'Place1'. Current character list: {expected_characters}"
    )


# Test execute raises PlaceCharacterAtPlaceError for invalid place type (e.g., REGION)
def test_execute_invalid_place_type_region(
    mock_playthrough_manager, mock_map_repository
):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data("Place1", TemplateType.REGION.value)
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(PlaceCharacterAtPlaceError) as exc_info:
        command.execute()

    assert "cannot house characters" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Test execute handles empty characters list correctly
def test_execute_with_empty_characters_list(
    mock_playthrough_manager, mock_map_repository
):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data(
        "Place1", TemplateType.LOCATION.value, characters=[]
    )
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with patch(
        "src.movements.commands.place_character_at_place_command.logger"
    ) as mock_logger:
        command.execute()

    assert map_data["Place1"]["characters"] == ["Char1"]
    mock_map_repository.save_map_data.assert_called_once_with(map_data)
    mock_logger.info.assert_called_once()


# Test execute raises PlaceCharacterAtPlaceError if place type is invalid (e.g., STORY_UNIVERSE)
def test_execute_invalid_place_type_story_universe(
    mock_playthrough_manager, mock_map_repository
):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data("Place1", TemplateType.STORY_UNIVERSE.value)
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(PlaceCharacterAtPlaceError) as exc_info:
        command.execute()

    assert "cannot house characters" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Test execute when map_repository.save_map_data raises an exception
def test_execute_save_map_data_exception(mock_playthrough_manager, mock_map_repository):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data(
        "Place1", TemplateType.ROOM.value, characters=["Char2"]
    )
    mock_map_repository.load_map_data.return_value = map_data
    mock_map_repository.save_map_data.side_effect = Exception("Save failed")

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(Exception) as exc_info:
        command.execute()

    assert "Save failed" in str(exc_info.value)
    assert "Char1" in map_data["Place1"]["characters"]
    mock_map_repository.load_map_data.assert_called_once()
    mock_map_repository.save_map_data.assert_called_once_with(map_data)


# Test execute when PlaythroughManager.get_followers returns empty list
def test_execute_no_followers(mock_playthrough_manager, mock_map_repository):
    mock_playthrough_manager.get_followers.return_value = []
    map_data = create_valid_map_data(
        "Place1", TemplateType.AREA.value, characters=["Char2"]
    )
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with patch(
        "src.movements.commands.place_character_at_place_command.logger"
    ) as mock_logger:
        command.execute()

    assert "Char1" in map_data["Place1"]["characters"]
    mock_map_repository.save_map_data.assert_called_once_with(map_data)
    mock_logger.info.assert_called_once()


# Test execute with multiple followers but character is not a follower
def test_execute_character_not_follower_with_multiple_followers(
    mock_playthrough_manager, mock_map_repository
):
    mock_playthrough_manager.get_followers.return_value = ["Char2", "Char3"]
    map_data = create_valid_map_data(
        "Place1", TemplateType.ROOM.value, characters=["Char2"]
    )
    mock_map_repository.load_map_data.return_value = map_data

    command = PlaceCharacterAtPlaceCommand(
        playthrough_name="TestPlaythrough",
        character_identifier="Char1",
        place_identifier="Place1",
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with patch(
        "src.movements.commands.place_character_at_place_command.logger"
    ) as mock_logger:
        command.execute()

    assert "Char1" in map_data["Place1"]["characters"]
    mock_map_repository.save_map_data.assert_called_once_with(map_data)
    mock_logger.info.assert_called_once()
