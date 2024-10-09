from unittest.mock import MagicMock, patch

from src.voices.providers.matching_voice_model_provider import (
    MatchingVoiceModelProvider,
)


# Test when a valid speaker is matched
def test_matching_speaker_valid_match():
    # Mock possible_speakers data
    possible_speakers = {
        "speaker1": [
            "male",
            "adult",
            "happy",
            "normal_tempo",
            "normal_volume",
            "smooth",
            "formal",
            "confident",
            "none",
        ],
    }

    # Mock FilesystemManager to return possible_speakers
    mock_filesystem_manager = MagicMock()
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        possible_speakers
    )

    # Define character_voice_attributes that match speaker1
    character_voice_attributes = {
        "voice_gender": "male",
        "voice_age": "adult",
        "voice_emotion": "happy",
        "voice_tempo": "normal_tempo",
        "voice_volume": "normal_volume",
        "voice_texture": "smooth",
        "voice_style": "formal",
        "voice_personality": "confident",
        "voice_special_effects": "none",
    }

    # Create an instance of MatchingSpeakerFactory with the mocked FilesystemManager
    factory = MatchingVoiceModelProvider(
        character_voice_attributes, filesystem_manager=mock_filesystem_manager
    )

    # Call match_speaker
    product = factory.match_speaker()

    # Assert that the product is valid and the matched speaker is speaker1
    assert product.is_valid()
    assert product.get() == "speaker1"
    assert product.get_error() is None


# Test when the optional attributes do not narrow down the speakers
def test_matching_speaker_optional_narrowing_no_match():
    # Mock possible_speakers data
    possible_speakers = {
        "speaker1": [
            "male",
            "adult",
            "happy",
            "normal_tempo",
            "normal_volume",
            "smooth",
            "formal",
            "confident",
            "none",
        ],
        "speaker2": [
            "male",
            "adult",
            "sad",
            "normal_tempo",
            "normal_volume",
            "smooth",
            "formal",
            "confident",
            "none",
        ],
    }

    # Mock FilesystemManager to return possible_speakers
    mock_filesystem_manager = MagicMock()
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        possible_speakers
    )

    # Define character_voice_attributes with a non-matching optional attribute
    character_voice_attributes = {
        "voice_gender": "male",
        "voice_age": "adult",
        "voice_emotion": "excited",  # No speaker has 'excited' emotion
        "voice_tempo": "normal_tempo",
        "voice_volume": "normal_volume",
        "voice_texture": "smooth",
        "voice_style": "formal",
        "voice_personality": "confident",
        "voice_special_effects": "none",
    }

    # Create an instance of MatchingSpeakerFactory with the mocked FilesystemManager
    factory = MatchingVoiceModelProvider(
        character_voice_attributes, filesystem_manager=mock_filesystem_manager
    )

    # Call match_speaker
    product = factory.match_speaker()

    # Assert that the product is valid and a speaker is matched
    assert product.is_valid()
    assert product.get() in possible_speakers
    assert product.get_error() is None


# Test when the optional attributes narrow down to a specific speaker
def test_matching_speaker_optional_narrowing_with_match():
    # Mock possible_speakers data
    possible_speakers = {
        "speaker1": [
            "male",
            "adult",
            "happy",
            "normal_tempo",
            "normal_volume",
            "smooth",
            "formal",
            "confident",
            "none",
        ],
        "speaker2": [
            "male",
            "adult",
            "sad",
            "normal_tempo",
            "normal_volume",
            "smooth",
            "formal",
            "confident",
            "none",
        ],
    }

    # Mock FilesystemManager to return possible_speakers
    mock_filesystem_manager = MagicMock()
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        possible_speakers
    )

    # Patch random.choice to always return 'speaker2'
    with patch("random.choice", return_value="speaker2"):
        # Define character_voice_attributes that match only speaker2
        character_voice_attributes = {
            "voice_gender": "male",
            "voice_age": "adult",
            "voice_emotion": "sad",  # Matches only speaker2
            "voice_tempo": "normal_tempo",
            "voice_volume": "normal_volume",
            "voice_texture": "smooth",
            "voice_style": "formal",
            "voice_personality": "confident",
            "voice_special_effects": "none",
        }

        # Create an instance of MatchingSpeakerFactory with the mocked FilesystemManager
        factory = MatchingVoiceModelProvider(
            character_voice_attributes, filesystem_manager=mock_filesystem_manager
        )

        # Call match_speaker
        product = factory.match_speaker()

        # Assert that the product is valid and the matched speaker is 'speaker2'
        assert product.is_valid()
        assert product.get() == "speaker2"
        assert product.get_error() is None


# Test when possible_speakers is empty
def test_matching_speaker_no_possible_speakers():
    # Mock possible_speakers data as empty
    possible_speakers = {}

    # Mock FilesystemManager to return possible_speakers
    mock_filesystem_manager = MagicMock()
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        possible_speakers
    )

    # Define character_voice_attributes
    character_voice_attributes = {
        "voice_gender": "male",
        "voice_age": "adult",
        "voice_emotion": "happy",
        "voice_tempo": "normal_tempo",
        "voice_volume": "normal_volume",
        "voice_texture": "smooth",
        "voice_style": "formal",
        "voice_personality": "confident",
        "voice_special_effects": "none",
    }

    # Create an instance of MatchingSpeakerFactory with the mocked FilesystemManager
    factory = MatchingVoiceModelProvider(
        character_voice_attributes, filesystem_manager=mock_filesystem_manager
    )

    # Call match_speaker
    product = factory.match_speaker()

    # Assert that the product is invalid with the appropriate error
    assert not product.is_valid()
    assert product.get() is None
    assert product.get_error() == "No matching voice models found."


# Test multiple matching speakers and control randomness
def test_matching_speaker_multiple_matches():
    # Mock possible_speakers data
    possible_speakers = {
        "speaker1": [
            "male",
            "adult",
            "happy",
            "normal_tempo",
            "normal_volume",
            "smooth",
            "formal",
            "confident",
            "none",
        ],
        "speaker2": [
            "male",
            "adult",
            "happy",
            "normal_tempo",
            "normal_volume",
            "smooth",
            "formal",
            "confident",
            "none",
        ],
        "speaker3": [
            "male",
            "adult",
            "happy",
            "normal_tempo",
            "normal_volume",
            "smooth",
            "formal",
            "confident",
            "none",
        ],
    }

    # Mock FilesystemManager to return possible_speakers
    mock_filesystem_manager = MagicMock()
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        possible_speakers
    )

    # Patch random.choice to always return 'speaker2'
    with patch("random.choice", return_value="speaker2"):
        # Define character_voice_attributes that match all speakers
        character_voice_attributes = {
            "voice_gender": "male",
            "voice_age": "adult",
            "voice_emotion": "happy",
            "voice_tempo": "normal_tempo",
            "voice_volume": "normal_volume",
            "voice_texture": "smooth",
            "voice_style": "formal",
            "voice_personality": "confident",
            "voice_special_effects": "none",
        }

        # Create an instance of MatchingSpeakerFactory with the mocked FilesystemManager
        factory = MatchingVoiceModelProvider(
            character_voice_attributes, filesystem_manager=mock_filesystem_manager
        )

        # Call match_speaker
        product = factory.match_speaker()

        # Assert that the product is valid and the matched speaker is 'speaker2'
        assert product.is_valid()
        assert product.get() == "speaker2"
        assert product.get_error() is None
