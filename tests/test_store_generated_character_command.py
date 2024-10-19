from unittest.mock import Mock, patch

import pytest

from src.base.enums import IdentifierType
from src.characters.commands.store_generated_character_command import (
    StoreGeneratedCharacterCommand,
)


# Helper function to generate valid character data
def get_valid_character_data():
    return {
        "name": "TestCharacter",
        "description": "A test character",
        "personality": "Testy",
        "profile": "Test profile",
        "likes": "Testing",
        "dislikes": "Bugs",
        "secrets": "None",
        "speech_patterns": [f"Pattern {i}" for i in range(10)],
        "health": "Healthy",
        "equipment": "Test equipment",
        "voice_gender": "Neutral",
        "voice_age": "Adult",
        "voice_emotion": "Neutral",
        "voice_tempo": "Normal",
        "voice_volume": "Medium",
        "voice_texture": "Smooth",
        "voice_tone": "Normal",
        "voice_style": "Plain",
        "voice_personality": "Friendly",
        "voice_special_effects": "None",
    }


def test_init_with_empty_character_data():
    # Arrange
    playthrough_name = Mock()
    playthrough_name.value = "TestPlaythrough"
    character_data = {}
    match_voice_data_to_voice_model_algorithm = Mock()

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        StoreGeneratedCharacterCommand(
            playthrough_name,
            character_data,
            match_voice_data_to_voice_model_algorithm,
        )
    assert "character_data can't be empty." in str(excinfo.value)


def test_init_with_empty_character_name():
    # Arrange
    playthrough_name = Mock()
    playthrough_name.value = "TestPlaythrough"
    character_data = {"name": "", "description": "desc", "personality": "pers"}
    match_voice_data_to_voice_model_algorithm = Mock()

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        StoreGeneratedCharacterCommand(
            playthrough_name,
            character_data,
            match_voice_data_to_voice_model_algorithm,
        )
    assert "malformed character_data." in str(excinfo.value)


def test_init_with_valid_character_data():
    # Arrange
    playthrough_name = Mock()
    playthrough_name.value = "TestPlaythrough"
    character_data = get_valid_character_data()
    match_voice_data_to_voice_model_algorithm = Mock()

    # Act
    cmd = StoreGeneratedCharacterCommand(
        playthrough_name,
        character_data,
        match_voice_data_to_voice_model_algorithm,
    )

    # Assert
    assert cmd._playthrough_name == playthrough_name
    assert cmd._character_data.name == "TestCharacter"


@patch("src.filesystem.filesystem_manager.FilesystemManager")
@patch("src.base.identifiers_manager.IdentifiersManager")
def test_execute_calls_filesystem_manager_methods(
    mock_identifiers_manager_class, mock_filesystem_manager_class
):
    # Arrange
    playthrough_name = Mock()
    playthrough_name.value = "TestPlaythrough"
    character_data = get_valid_character_data()
    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.return_value = "TestVoiceModel"

    mock_filesystem_manager = mock_filesystem_manager_class.return_value
    mock_filesystem_manager.get_file_path_to_characters_file.return_value = (
        "characters.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}

    mock_identifiers_manager = mock_identifiers_manager_class.return_value
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = "1"

    cmd = StoreGeneratedCharacterCommand(
        playthrough_name,
        character_data,
        match_voice_data_to_voice_model_algorithm,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Act
    cmd.execute()

    # Assert
    mock_filesystem_manager.get_file_path_to_characters_file.assert_called_once_with(
        "TestPlaythrough"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once_with(
        "characters.json"
    )
    mock_identifiers_manager.produce_and_update_next_identifier.assert_called_once_with(
        IdentifierType.CHARACTERS
    )
    mock_filesystem_manager.save_json_file.assert_called_once()
    args, _ = mock_filesystem_manager.save_json_file.call_args
    saved_characters, characters_file = args
    assert characters_file == "characters.json"
    assert "1" in saved_characters
    assert saved_characters["1"]["name"] == "TestCharacter"
    assert saved_characters["1"]["voice_model"] == "TestVoiceModel"


def test_compose_speech_patterns():
    # Arrange
    playthrough_name = Mock()
    playthrough_name.value = "TestPlaythrough"
    character_data = get_valid_character_data()
    cmd = StoreGeneratedCharacterCommand(playthrough_name, character_data, Mock())

    # Act
    speech_patterns = cmd._compose_speech_patterns()

    # Assert
    expected_speech_patterns = "\n".join(
        [f"TestCharacter: Pattern {i}" for i in range(10)]
    )
    assert speech_patterns == expected_speech_patterns


@patch("src.filesystem.filesystem_manager.FilesystemManager")
@patch("src.base.identifiers_manager.IdentifiersManager")
def test_execute_with_existing_characters(
    mock_identifiers_manager_class, mock_filesystem_manager_class
):
    # Arrange
    playthrough_name = Mock()
    playthrough_name.value = "TestPlaythrough"
    character_data = get_valid_character_data()
    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.return_value = "TestVoiceModel"

    existing_characters = {
        "1": {"name": "ExistingCharacter", "description": "Existing description"}
    }

    mock_filesystem_manager = mock_filesystem_manager_class.return_value
    mock_filesystem_manager.get_file_path_to_characters_file.return_value = (
        "characters.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        existing_characters
    )

    mock_identifiers_manager = mock_identifiers_manager_class.return_value
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = "2"

    cmd = StoreGeneratedCharacterCommand(
        playthrough_name,
        character_data,
        match_voice_data_to_voice_model_algorithm,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Act
    cmd.execute()

    # Assert
    mock_filesystem_manager.save_json_file.assert_called_once()
    args, _ = mock_filesystem_manager.save_json_file.call_args
    saved_characters, _ = args
    assert "1" in saved_characters
    assert "2" in saved_characters
    assert saved_characters["2"]["name"] == "TestCharacter"


def test_execute_with_no_matching_voice_model():
    # Arrange
    playthrough_name = Mock()
    playthrough_name.value = "TestPlaythrough"
    character_data = get_valid_character_data()
    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.return_value = (
        None  # Simulate no match
    )

    mock_filesystem_manager = Mock()
    mock_filesystem_manager.get_file_path_to_characters_file.return_value = (
        "characters.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}

    mock_identifiers_manager = Mock()
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = "1"

    cmd = StoreGeneratedCharacterCommand(
        playthrough_name,
        character_data,
        match_voice_data_to_voice_model_algorithm,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Act
    cmd.execute()

    # Assert
    args, _ = mock_filesystem_manager.save_json_file.call_args
    saved_characters, _ = args
    assert (
        saved_characters["1"]["voice_model"] is None
    )  # or DEFAULT_VOICE_MODEL if applicable


def test_execute_logs_info_message(caplog):
    # Arrange
    playthrough_name = Mock()
    playthrough_name.value = "TestPlaythrough"
    character_data = get_valid_character_data()
    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.return_value = "TestVoiceModel"

    mock_filesystem_manager = Mock()
    mock_filesystem_manager.get_file_path_to_characters_file.return_value = (
        "characters.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}

    mock_identifiers_manager = Mock()
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = "1"

    cmd = StoreGeneratedCharacterCommand(
        playthrough_name,
        character_data,
        match_voice_data_to_voice_model_algorithm,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Act
    with caplog.at_level("INFO"):
        cmd.execute()

    # Assert
    assert any(
        "Saved character 'TestCharacter' at 'characters.json'" in message
        for message in caplog.text.splitlines()
    )
