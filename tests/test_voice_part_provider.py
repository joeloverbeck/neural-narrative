# test_voice_part_provider.py

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.base.exceptions import VoiceLineGenerationError
from src.filesystem.config_loader import ConfigLoader
from src.voices.factories.generate_voice_line_algorithm_factory import (
    GenerateVoiceLineAlgorithmFactory,
)
from src.voices.providers.voice_part_provider import (
    VoicePartProvider,
    VoicePartProviderConfig,
)


# Sample configuration for VoicePartProviderConfig
@pytest.fixture
def voice_part_provider_config():
    return VoicePartProviderConfig(
        part="Hello, World!",
        xtts_endpoint="http://example.com/xtts",
        timestamp="20231028T123000",
        index=1,
        temp_dir=Path("/tmp"),
    )


# Mock ConfigLoader
@pytest.fixture
def mock_config_loader():
    mock = Mock(spec=ConfigLoader)
    mock.get_narrator_voice_model.return_value = "narrator_voice_model"
    return mock


# Mock GenerateVoiceLineAlgorithmFactory
@pytest.fixture
def mock_algorithm_factory():
    factory = Mock(spec=GenerateVoiceLineAlgorithmFactory)
    mock_algorithm = Mock()
    factory.create_algorithm.return_value = mock_algorithm
    return factory, mock_algorithm


# Test when part is empty
def test_create_voice_part_empty_part(
    voice_part_provider_config, mock_config_loader, mock_algorithm_factory
):
    voice_part_provider_config.part = "   "  # Only whitespace
    factory, mock_algorithm = mock_algorithm_factory

    provider = VoicePartProvider(
        character_name="Character",
        voice_model="default_voice",
        voice_part_provider_config=voice_part_provider_config,
        generate_voice_line_algorithm_factory=factory,
        config_loader=mock_config_loader,
    )

    result = provider.create_voice_part()
    assert result is None
    factory.create_algorithm.assert_not_called()
    mock_algorithm.generate_voice_line.assert_not_called()


# Test when part starts and ends with *
def test_create_voice_part_narrator_voice(
    voice_part_provider_config, mock_config_loader, mock_algorithm_factory
):
    voice_part_provider_config.part = "*This is a narrator line.*"
    factory, mock_algorithm = mock_algorithm_factory

    provider = VoicePartProvider(
        character_name="Narrator",
        voice_model="default_voice",
        voice_part_provider_config=voice_part_provider_config,
        generate_voice_line_algorithm_factory=factory,
        config_loader=mock_config_loader,
    )

    result = provider.create_voice_part()
    assert result == Path("/tmp/20231028T123000_Narrator_narrator_voice_model_1.wav")
    factory.create_algorithm.assert_called_once_with(
        "This is a narrator line.",
        "narrator_voice_model",
        "http://example.com/xtts",
        result,
    )
    mock_algorithm.generate_voice_line.assert_called_once()


# Test when part does not start and end with *
def test_create_voice_part_default_voice(
    voice_part_provider_config, mock_config_loader, mock_algorithm_factory
):
    voice_part_provider_config.part = "Hello, this is a character."
    factory, mock_algorithm = mock_algorithm_factory

    provider = VoicePartProvider(
        character_name="Character",
        voice_model="default_voice",
        voice_part_provider_config=voice_part_provider_config,
        generate_voice_line_algorithm_factory=factory,
        config_loader=mock_config_loader,
    )

    result = provider.create_voice_part()
    assert result == Path("/tmp/20231028T123000_Character_default_voice_1.wav")
    factory.create_algorithm.assert_called_once_with(
        "Hello, this is a character.",
        "default_voice",
        "http://example.com/xtts",
        result,
    )
    mock_algorithm.generate_voice_line.assert_called_once()


# Test when part is only * with no text
def test_create_voice_part_only_asterisks(
    voice_part_provider_config, mock_config_loader, mock_algorithm_factory
):
    voice_part_provider_config.part = "**"
    factory, mock_algorithm = mock_algorithm_factory

    provider = VoicePartProvider(
        character_name="Character",
        voice_model="default_voice",
        voice_part_provider_config=voice_part_provider_config,
        generate_voice_line_algorithm_factory=factory,
        config_loader=mock_config_loader,
    )

    result = provider.create_voice_part()
    assert result is None
    factory.create_algorithm.assert_not_called()
    mock_algorithm.generate_voice_line.assert_not_called()


# Test temp_file_path construction
def test_create_voice_part_temp_file_path(
    voice_part_provider_config, mock_config_loader, mock_algorithm_factory
):
    voice_part_provider_config.part = "Sample dialogue."
    factory, mock_algorithm = mock_algorithm_factory

    provider = VoicePartProvider(
        character_name="Hero",
        voice_model="hero_voice",
        voice_part_provider_config=voice_part_provider_config,
        generate_voice_line_algorithm_factory=factory,
        config_loader=mock_config_loader,
    )

    result = provider.create_voice_part()
    expected_path = Path("/tmp/20231028T123000_Hero_hero_voice_1.wav")
    assert result == expected_path
    factory.create_algorithm.assert_called_once_with(
        "Sample dialogue.",
        "hero_voice",
        "http://example.com/xtts",
        expected_path,
    )


# Test exception handling during voice line generation
def test_create_voice_part_algorithm_exception(
    voice_part_provider_config, mock_config_loader, mock_algorithm_factory
):
    voice_part_provider_config.part = "Error generating voice."
    factory, mock_algorithm = mock_algorithm_factory
    mock_algorithm.generate_voice_line.side_effect = Exception("Generation failed")

    provider = VoicePartProvider(
        character_name="Character",
        voice_model="default_voice",
        voice_part_provider_config=voice_part_provider_config,
        generate_voice_line_algorithm_factory=factory,
        config_loader=mock_config_loader,
    )

    with pytest.raises(VoiceLineGenerationError) as exc_info:
        provider.create_voice_part()

    assert "Error generating voice line for part 1: Generation failed" in str(
        exc_info.value
    )
    factory.create_algorithm.assert_called_once()
    mock_algorithm.generate_voice_line.assert_called_once()


# Test successful voice line generation
def test_create_voice_part_success(
    voice_part_provider_config, mock_config_loader, mock_algorithm_factory
):
    voice_part_provider_config.part = "Successful generation."
    factory, mock_algorithm = mock_algorithm_factory
    # No exception is raised, simulating successful generation

    provider = VoicePartProvider(
        character_name="Protagonist",
        voice_model="protagonist_voice",
        voice_part_provider_config=voice_part_provider_config,
        generate_voice_line_algorithm_factory=factory,
        config_loader=mock_config_loader,
    )

    result = provider.create_voice_part()
    expected_path = Path("/tmp/20231028T123000_Protagonist_protagonist_voice_1.wav")
    assert result == expected_path
    factory.create_algorithm.assert_called_once_with(
        "Successful generation.",
        "protagonist_voice",
        "http://example.com/xtts",
        result,
    )
    mock_algorithm.generate_voice_line.assert_called_once()


# Test when ConfigLoader is not provided (uses default)
def test_create_voice_part_default_config_loader(
    voice_part_provider_config, mock_algorithm_factory
):
    with patch(
        "src.voices.providers.voice_part_provider.ConfigLoader"
    ) as MockConfigLoader:
        mock_config_loader_instance = MockConfigLoader.return_value
        mock_config_loader_instance.get_narrator_voice_model.return_value = (
            "narrator_default"
        )
        voice_part_provider_config.part = "*Narrator speaks.*"

        factory, mock_algorithm = mock_algorithm_factory

        provider = VoicePartProvider(
            character_name="Narrator",
            voice_model="default_voice",
            voice_part_provider_config=voice_part_provider_config,
            generate_voice_line_algorithm_factory=factory,
            config_loader=None,  # Not provided, should use default
        )

        result = provider.create_voice_part()
        assert result == Path("/tmp/20231028T123000_Narrator_narrator_default_1.wav")
        MockConfigLoader.assert_called_once()
        mock_config_loader_instance.get_narrator_voice_model.assert_called_once()
        factory.create_algorithm.assert_called_once_with(
            "Narrator speaks.",
            "narrator_default",
            "http://example.com/xtts",
            result,
        )
        mock_algorithm.generate_voice_line.assert_called_once()
