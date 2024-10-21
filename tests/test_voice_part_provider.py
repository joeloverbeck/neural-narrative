import os
from unittest.mock import MagicMock

import pytest

from src.base.constants import NARRATOR_VOICE_MODEL
from src.base.exceptions import VoiceLineGenerationError
from src.base.required_string import RequiredString
from src.voices.configs.voice_part_provider_config import VoicePartProviderConfig
from src.voices.factories.generate_voice_line_algorithm_factory import (
    GenerateVoiceLineAlgorithmFactory,
)
# Import the classes and exceptions we need to test
from src.voices.providers.voice_part_provider import VoicePartProvider


# Helper function to create a default config
def create_default_config(**overrides):
    config = VoicePartProviderConfig(
        part=overrides.get("part", "Hello, world!"),
        xtts_endpoint=overrides.get("xtts_endpoint", "http://test-endpoint"),
        timestamp=overrides.get("timestamp", "1234567890"),
        index=overrides.get("index", 0),
        temp_dir=RequiredString(overrides.get("temp_dir", "/tmp")),
        temp_file_paths=overrides.get("temp_file_paths", []),
    )
    return config


# Test when part is empty or whitespace only
def test_create_voice_part_empty_part():
    config = create_default_config(part="   ")
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    provider = VoicePartProvider(
        RequiredString("Character Name"), RequiredString("voicemodel"), config, factory
    )

    provider.create_voice_part()

    # Ensure no algorithm is created and temp_file_paths remains empty
    factory.create_algorithm.assert_not_called()
    assert config.temp_file_paths == []


# Test when part is enclosed in asterisks (uses NARRATOR_VOICE_MODEL)
def test_create_voice_part_narrator_voice():
    config = create_default_config(part="*This is narrator text*")
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    algorithm_mock = MagicMock()
    factory.create_algorithm.return_value = algorithm_mock

    provider = VoicePartProvider(
        RequiredString("Character Name"), RequiredString("voicemodel"), config, factory
    )

    provider.create_voice_part()

    # Check that NARRATOR_VOICE_MODEL is used
    factory.create_algorithm.assert_called_once()
    args, kwargs = factory.create_algorithm.call_args
    assert args[1] == NARRATOR_VOICE_MODEL  # voice_to_use
    # Check that temp_file_path is appended
    assert len(config.temp_file_paths) == 1


# Test when part is normal text (uses voice_model from config)
def test_create_voice_part_normal_text():
    config = create_default_config(part="This is normal text")
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    algorithm_mock = MagicMock()
    factory.create_algorithm.return_value = algorithm_mock

    voice_model = RequiredString("voicemodel")

    provider = VoicePartProvider(
        RequiredString("Character Name"), voice_model, config, factory
    )

    provider.create_voice_part()

    # Check that voice_model from config is used
    factory.create_algorithm.assert_called_once()
    args, kwargs = factory.create_algorithm.call_args
    assert args[1] == voice_model
    # Check that temp_file_path is appended
    assert len(config.temp_file_paths) == 1


# Test when part becomes empty after stripping asterisks
def test_create_voice_part_empty_after_stripping():
    config = create_default_config(part="*   *")
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    provider = VoicePartProvider(
        RequiredString("Character Name"), RequiredString("voicemodel"), config, factory
    )

    provider.create_voice_part()

    # Ensure no algorithm is created and temp_file_paths remains empty
    factory.create_algorithm.assert_not_called()
    assert config.temp_file_paths == []


# Test exception handling when generate_voice_line raises an exception
def test_create_voice_part_generation_exception():
    config = create_default_config()
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    algorithm_mock = MagicMock()
    algorithm_mock.generate_voice_line.side_effect = Exception("Generation failed")
    factory.create_algorithm.return_value = algorithm_mock

    provider = VoicePartProvider(
        RequiredString("Character Name"), RequiredString("voicemodel"), config, factory
    )

    with pytest.raises(VoiceLineGenerationError) as exc_info:
        provider.create_voice_part()

    # Check that the exception message contains the index
    assert str(config.index) in str(exc_info.value)
    # Ensure temp_file_paths remains empty
    assert config.temp_file_paths == []


# Test that temp_file_path is appended when generation is successful
def test_create_voice_part_appends_temp_file_path():
    config = create_default_config()
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    algorithm_mock = MagicMock()
    factory.create_algorithm.return_value = algorithm_mock

    character_name = RequiredString("Character Name")
    voice_model = RequiredString("voicemodel")

    provider = VoicePartProvider(character_name, voice_model, config, factory)

    provider.create_voice_part()

    # Check that temp_file_path is appended
    assert len(config.temp_file_paths) == 1
    expected_temp_file_name = (
        f"{config.timestamp}_{character_name}_{voice_model}_{config.index}.wav"
    )
    expected_temp_file_path = os.path.join(
        config.temp_dir.value, expected_temp_file_name
    )
    assert config.temp_file_paths[0] == expected_temp_file_path


# Test VoicePartProviderConfig validation
def test_voice_part_provider_config_validation():
    # Test empty xtts_endpoint
    with pytest.raises(ValueError, match="xtts_endpoint can't be empty."):
        create_default_config(xtts_endpoint="")

    # Test empty timestamp
    with pytest.raises(ValueError, match="timestamp can't be empty."):
        create_default_config(timestamp="")

    # Test negative index
    with pytest.raises(ValueError, match="Invalid index: -1."):
        create_default_config(index=-1)

    # Valid configuration does not raise exceptions
    config = create_default_config()
    assert config.part == "Hello, world!"
