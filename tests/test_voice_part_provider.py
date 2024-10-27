import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.base.exceptions import VoiceLineGenerationError
from src.voices.configs.voice_part_provider_config import VoicePartProviderConfig
from src.voices.factories.generate_voice_line_algorithm_factory import (
    GenerateVoiceLineAlgorithmFactory,
)
from src.voices.providers.voice_part_provider import VoicePartProvider


def create_default_config(**overrides):
    config = VoicePartProviderConfig(
        part=overrides.get("part", "Hello, world!"),
        xtts_endpoint=overrides.get("xtts_endpoint", "http://test-endpoint"),
        timestamp=overrides.get("timestamp", "1234567890"),
        index=overrides.get("index", 0),
        temp_dir=Path(overrides.get("temp_dir", "/tmp")),
        temp_file_paths=overrides.get("temp_file_paths", []),
    )
    return config


def test_create_voice_part_empty_part():
    config = create_default_config(part="   ")
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    provider = VoicePartProvider("Character Name", "voicemodel", config, factory)
    provider.create_voice_part()
    factory.create_algorithm.assert_not_called()
    assert config.temp_file_paths == []


def test_create_voice_part_narrator_voice():
    config = create_default_config(part="*This is narrator text*")
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    algorithm_mock = MagicMock()
    factory.create_algorithm.return_value = algorithm_mock
    provider = VoicePartProvider("Character Name", "voicemodel", config, factory)
    provider.create_voice_part()
    factory.create_algorithm.assert_called_once()
    _args, _kwargs = factory.create_algorithm.call_args
    assert len(config.temp_file_paths) == 1


def test_create_voice_part_normal_text():
    config = create_default_config(part="This is normal text")
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    algorithm_mock = MagicMock()
    factory.create_algorithm.return_value = algorithm_mock
    voice_model = "voicemodel"
    provider = VoicePartProvider("Character Name", voice_model, config, factory)
    provider.create_voice_part()
    factory.create_algorithm.assert_called_once()
    args, kwargs = factory.create_algorithm.call_args
    assert args[1] == voice_model
    assert len(config.temp_file_paths) == 1


def test_create_voice_part_empty_after_stripping():
    config = create_default_config(part="*   *")
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    provider = VoicePartProvider("Character Name", "voicemodel", config, factory)
    provider.create_voice_part()
    factory.create_algorithm.assert_not_called()
    assert config.temp_file_paths == []


def test_create_voice_part_generation_exception():
    config = create_default_config()
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    algorithm_mock = MagicMock()
    algorithm_mock.generate_voice_line.side_effect = Exception("Generation failed")
    factory.create_algorithm.return_value = algorithm_mock
    provider = VoicePartProvider("Character Name", "voicemodel", config, factory)
    with pytest.raises(VoiceLineGenerationError) as exc_info:
        provider.create_voice_part()
    assert str(config.index) in str(exc_info)
    assert config.temp_file_paths == []


def test_create_voice_part_appends_temp_file_path():
    config = create_default_config()
    factory = MagicMock(spec=GenerateVoiceLineAlgorithmFactory)
    algorithm_mock = MagicMock()
    factory.create_algorithm.return_value = algorithm_mock
    character_name = "Character Name"
    voice_model = "voicemodel"
    provider = VoicePartProvider(character_name, voice_model, config, factory)
    provider.create_voice_part()
    assert len(config.temp_file_paths) == 1
    expected_temp_file_name = (
        f"{config.timestamp}_{character_name}_{voice_model}_{config.index}.wav"
    )
    expected_temp_file_path = os.path.join(config.temp_dir, expected_temp_file_name)
    assert config.temp_file_paths[0] == expected_temp_file_path


def test_voice_part_provider_config_validation():
    with pytest.raises(ValueError, match="xtts_endpoint can't be empty."):
        create_default_config(xtts_endpoint="")
    with pytest.raises(ValueError, match="timestamp can't be empty."):
        create_default_config(timestamp="")
    with pytest.raises(ValueError, match="Invalid index: -1."):
        create_default_config(index=-1)
    config = create_default_config()
    assert config.part == "Hello, world!"
