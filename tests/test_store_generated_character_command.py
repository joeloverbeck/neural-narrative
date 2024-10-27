from unittest.mock import Mock, patch

import pytest

from src.characters.commands.store_generated_character_command import (
    StoreGeneratedCharacterCommand,
)
from src.voices.voice_attributes import VoiceAttributes


def valid_character_data():
    return {
        "name": "Test Character",
        "description": "A character for testing.",
        "personality": "Testy",
        "profile": "Tester",
        "likes": "Testing",
        "dislikes": "Not testing",
        "secrets": "None",
        "speech_patterns": ["Hello"] * 10,
        "health": "Good",
        "equipment": "Test Equipment",
        "voice_gender": "Male",
        "voice_age": "Adult",
        "voice_emotion": "Neutral",
        "voice_tempo": "Normal",
        "voice_volume": "Medium",
        "voice_texture": "Smooth",
        "voice_tone": "Calm",
        "voice_style": "Standard",
        "voice_personality": "Professional",
        "voice_special_effects": "None",
    }


def test_store_generated_character_command_init_valid():
    character_data = valid_character_data()
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    produce_and_update_next_identifier_algorithm = Mock()

    command = StoreGeneratedCharacterCommand(
        playthrough_name,
        character_data,
        match_voice_data_to_voice_model_algorithm,
        produce_and_update_next_identifier_algorithm,
    )

    assert command._playthrough_name == playthrough_name
    assert command._character_data.name == "Test Character"


def test_store_generated_character_command_init_empty_character_data():
    character_data = {}
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    produce_and_update_next_identifier_algorithm = Mock()

    with pytest.raises(ValueError) as excinfo:
        StoreGeneratedCharacterCommand(
            playthrough_name,
            character_data,
            match_voice_data_to_voice_model_algorithm,
            produce_and_update_next_identifier_algorithm,
        )
    assert str(excinfo.value) == "character_data can't be empty."


def test_store_generated_character_command_init_empty_name():
    character_data = valid_character_data()
    character_data["name"] = ""
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    produce_and_update_next_identifier_algorithm = Mock()

    with pytest.raises(ValueError) as excinfo:
        StoreGeneratedCharacterCommand(
            playthrough_name,
            character_data,
            match_voice_data_to_voice_model_algorithm,
            produce_and_update_next_identifier_algorithm,
        )
    assert str(excinfo.value) == "malformed character_data."


def test_store_generated_character_command_init_missing_name_key():
    character_data = valid_character_data()
    del character_data["name"]
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    produce_and_update_next_identifier_algorithm = Mock()

    with pytest.raises(KeyError):
        StoreGeneratedCharacterCommand(
            playthrough_name,
            character_data,
            match_voice_data_to_voice_model_algorithm,
            produce_and_update_next_identifier_algorithm,
        )


def test_store_generated_character_command_init_missing_required_field():
    character_data = valid_character_data()
    del character_data["description"]
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    produce_and_update_next_identifier_algorithm = Mock()

    with pytest.raises(KeyError) as excinfo:
        StoreGeneratedCharacterCommand(
            playthrough_name,
            character_data,
            match_voice_data_to_voice_model_algorithm,
            produce_and_update_next_identifier_algorithm,
        )
    assert "description" in str(excinfo.value)


def test_store_generated_character_command_init_speech_patterns_wrong_length():
    character_data = valid_character_data()
    character_data["speech_patterns"] = ["Hello"] * 9  # Only 9 items
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    produce_and_update_next_identifier_algorithm = Mock()

    with pytest.raises(ValueError) as excinfo:
        StoreGeneratedCharacterCommand(
            playthrough_name,
            character_data,
            match_voice_data_to_voice_model_algorithm,
            produce_and_update_next_identifier_algorithm,
        )
    assert "CharacterData field 'speech_patterns' must have exactly 10 items." in str(
        excinfo.value
    )


def test_store_generated_character_command_execute():
    character_data = valid_character_data()
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.return_value = "TestVoiceModel"

    produce_and_update_next_identifier_algorithm = Mock()
    produce_and_update_next_identifier_algorithm.do_algorithm.return_value = (
        "character_1"
    )

    path_manager = Mock()
    path_manager.get_characters_file_path.return_value = "path/to/characters_file.json"

    expected_speech_patterns = "\n".join(["Test Character: Hello"] * 10)
    expected_modified_character_data = character_data.copy()
    expected_modified_character_data["speech_patterns"] = expected_speech_patterns
    expected_modified_character_data["voice_model"] = "TestVoiceModel"

    expected_characters_file = {"character_1": expected_modified_character_data}

    with patch(
        "src.characters.commands.store_generated_character_command.read_json_file",
        return_value={},
    ) as mock_read_json_file:
        with patch(
            "src.characters.commands.store_generated_character_command.write_json_file"
        ) as mock_write_json_file:
            command = StoreGeneratedCharacterCommand(
                playthrough_name,
                character_data,
                match_voice_data_to_voice_model_algorithm,
                produce_and_update_next_identifier_algorithm,
                path_manager=path_manager,
            )
            command.execute()

            mock_read_json_file.assert_called_once_with("path/to/characters_file.json")

            expected_voice_attributes = VoiceAttributes(
                "Male",
                "Adult",
                "Neutral",
                "Normal",
                "Medium",
                "Smooth",
                "Calm",
                "Standard",
                "Professional",
                "None",
            )
            match_voice_data_to_voice_model_algorithm.match.assert_called_once_with(
                expected_voice_attributes
            )

            produce_and_update_next_identifier_algorithm.do_algorithm.assert_called_once()

            mock_write_json_file.assert_called_once_with(
                "path/to/characters_file.json",
                expected_characters_file,
            )


def test_store_generated_character_command_compose_speech_patterns():
    character_data = valid_character_data()
    character_data["speech_patterns"] = [f"Pattern {i}" for i in range(1, 11)]
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    produce_and_update_next_identifier_algorithm = Mock()

    command = StoreGeneratedCharacterCommand(
        playthrough_name,
        character_data,
        match_voice_data_to_voice_model_algorithm,
        produce_and_update_next_identifier_algorithm,
    )

    composed_speech_patterns = command._compose_speech_patterns()

    expected_speech_patterns = "\n".join(
        [f"Test Character: Pattern {i}" for i in range(1, 11)]
    )

    assert composed_speech_patterns == expected_speech_patterns


def test_store_generated_character_command_execute_with_existing_characters():
    character_data = valid_character_data()
    playthrough_name = "TestPlaythrough"

    existing_characters = {
        "existing_character": {
            "name": "Existing Character",
            "description": "An existing character.",
            "personality": "Friendly",
            "profile": "NPC",
            "likes": "Helping",
            "dislikes": "Conflict",
            "secrets": "Unknown",
            "speech_patterns": "Existing speech patterns",
            "health": "Good",
            "equipment": "Standard Gear",
            "voice_gender": "Female",
            "voice_age": "Adult",
            "voice_emotion": "Happy",
            "voice_tempo": "Fast",
            "voice_volume": "Loud",
            "voice_texture": "Raspy",
            "voice_tone": "High",
            "voice_style": "Casual",
            "voice_personality": "Cheerful",
            "voice_special_effects": "Echo",
            "voice_model": "ExistingVoiceModel",
        }
    }

    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.return_value = "TestVoiceModel"

    produce_and_update_next_identifier_algorithm = Mock()
    produce_and_update_next_identifier_algorithm.do_algorithm.return_value = (
        "character_1"
    )

    path_manager = Mock()
    path_manager.get_characters_file_path.return_value = "path/to/characters_file.json"

    expected_speech_patterns = "\n".join(["Test Character: Hello"] * 10)
    expected_modified_character_data = character_data.copy()
    expected_modified_character_data["speech_patterns"] = expected_speech_patterns
    expected_modified_character_data["voice_model"] = "TestVoiceModel"

    expected_characters_file = existing_characters.copy()
    expected_characters_file["character_1"] = expected_modified_character_data

    with patch(
        "src.characters.commands.store_generated_character_command.read_json_file",
        return_value=existing_characters,
    ):
        with patch(
            "src.characters.commands.store_generated_character_command.write_json_file"
        ) as mock_write_json_file:
            command = StoreGeneratedCharacterCommand(
                playthrough_name,
                character_data,
                match_voice_data_to_voice_model_algorithm,
                produce_and_update_next_identifier_algorithm,
                path_manager=path_manager,
            )
            command.execute()

            mock_write_json_file.assert_called_once_with(
                "path/to/characters_file.json",
                expected_characters_file,
            )


def test_store_generated_character_command_execute_read_json_file_exception():
    character_data = valid_character_data()
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.return_value = "TestVoiceModel"

    produce_and_update_next_identifier_algorithm = Mock()
    produce_and_update_next_identifier_algorithm.do_algorithm.return_value = (
        "character_1"
    )

    path_manager = Mock()
    path_manager.get_characters_path.return_value = "path/to/characters_file.json"

    with patch(
        "src.characters.commands.store_generated_character_command.read_json_file",
        side_effect=FileNotFoundError,
    ):
        with patch(
            "src.characters.commands.store_generated_character_command.write_json_file"
        ):
            command = StoreGeneratedCharacterCommand(
                playthrough_name,
                character_data,
                match_voice_data_to_voice_model_algorithm,
                produce_and_update_next_identifier_algorithm,
                path_manager=path_manager,
            )

            with pytest.raises(FileNotFoundError):
                command.execute()


def test_store_generated_character_command_execute_match_voice_algorithm_exception():
    character_data = valid_character_data()
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.side_effect = Exception(
        "Match algorithm error"
    )

    produce_and_update_next_identifier_algorithm = Mock()
    produce_and_update_next_identifier_algorithm.do_algorithm.return_value = (
        "character_1"
    )

    path_manager = Mock()
    path_manager.get_characters_path.return_value = "path/to/characters_file.json"

    with patch(
        "src.characters.commands.store_generated_character_command.read_json_file",
        return_value={},
    ):
        with patch(
            "src.characters.commands.store_generated_character_command.write_json_file"
        ):
            command = StoreGeneratedCharacterCommand(
                playthrough_name,
                character_data,
                match_voice_data_to_voice_model_algorithm,
                produce_and_update_next_identifier_algorithm,
                path_manager=path_manager,
            )

            with pytest.raises(Exception) as excinfo:
                command.execute()
            assert "Match algorithm error" in str(excinfo.value)


def test_store_generated_character_command_execute_produce_identifier_exception():
    character_data = valid_character_data()
    playthrough_name = "TestPlaythrough"

    match_voice_data_to_voice_model_algorithm = Mock()
    match_voice_data_to_voice_model_algorithm.match.return_value = "TestVoiceModel"

    produce_and_update_next_identifier_algorithm = Mock()
    produce_and_update_next_identifier_algorithm.do_algorithm.side_effect = Exception(
        "Identifier algorithm error"
    )

    path_manager = Mock()
    path_manager.get_characters_path.return_value = "path/to/characters_file.json"

    with patch(
        "src.characters.commands.store_generated_character_command.read_json_file",
        return_value={},
    ):
        with patch(
            "src.characters.commands.store_generated_character_command.write_json_file"
        ):
            command = StoreGeneratedCharacterCommand(
                playthrough_name,
                character_data,
                match_voice_data_to_voice_model_algorithm,
                produce_and_update_next_identifier_algorithm,
                path_manager=path_manager,
            )

            with pytest.raises(Exception) as excinfo:
                command.execute()
            assert "Identifier algorithm error" in str(excinfo.value)
