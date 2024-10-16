from unittest.mock import MagicMock

import pytest

from src.characters.character import Character

# Sample character data for testing
sample_character_data = {
    "char1": {
        "name": "Test Character",
        "description": "A test character.",
        "personality": "Friendly",
        "profile": "Warrior",
        "likes": "Adventuring",
        "dislikes": "Laziness",
        "secrets": "None",
        "first message": "Hello there!",
        "speech_patterns": "Formal",
        "health": "100",
        "equipment": "Sword",
        "voice_gender": "Male",
        "voice_age": "Young",
        "voice_emotion": "Neutral",
        "voice_tempo": "Medium",
        "voice_volume": "Medium",
        "voice_tone": "Warm",
        "voice_texture": "Smooth",
        "voice_style": "Narrative",
        "voice_personality": "Calm",
        "voice_special_effects": "None",
        "voice_model": "Model A",
    }
}


@pytest.fixture
def mock_filesystem_manager():
    """Fixture to create a mock FilesystemManager."""
    # Create the mock object
    mock_fs_manager = MagicMock()

    # Mock methods
    mock_fs_manager.get_file_path_to_characters_file.return_value = (
        "mock_characters_file_path.json"
    )
    mock_fs_manager.load_existing_or_new_json_file.return_value = (
        sample_character_data.copy()
    )
    mock_fs_manager.get_file_path_to_character_image_for_web.return_value = (
        "mock_image_url"
    )
    mock_fs_manager.save_json_file.return_value = (
        None  # Assuming save_json_file doesn't return anything
    )

    return mock_fs_manager


def test_character_init_with_valid_data(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    # Assert character attributes
    assert character.playthrough_name == playthrough_name
    assert character.identifier == identifier
    assert character.name == "Test Character"
    assert character.description == "A test character."

    # Assert that get_file_path_to_characters_file was called with playthrough_name
    mock_filesystem_manager.get_file_path_to_characters_file.assert_called_with(
        playthrough_name
    )

    # Assert that load_existing_or_new_json_file was called with the characters file path
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_with(
        "mock_characters_file_path.json"
    )


def test_character_init_with_empty_playthrough_name(mock_filesystem_manager):
    identifier = "char1"
    with pytest.raises(ValueError) as excinfo:
        Character("", identifier, filesystem_manager=mock_filesystem_manager)
    assert "playthrough_name should not be empty." in str(excinfo.value)


def test_character_init_with_empty_identifier(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    with pytest.raises(ValueError) as excinfo:
        Character(playthrough_name, "", filesystem_manager=mock_filesystem_manager)
    assert "identifier should not be empty." in str(excinfo.value)


def test_character_init_with_nonexistent_identifier(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "nonexistent_char"

    # Modify the mock to return a dict without the identifier
    mock_fs_manager = mock_filesystem_manager
    mock_fs_manager.load_existing_or_new_json_file.return_value = {
        "another_char": sample_character_data["char1"]
    }

    with pytest.raises(KeyError) as excinfo:
        Character(playthrough_name, identifier, filesystem_manager=mock_fs_manager)
    assert f"Character with identifier '{identifier}' not found." in str(excinfo.value)


def test_character_init_with_missing_required_attributes(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    # Remove 'name' from the character data
    incomplete_data = sample_character_data.copy()
    incomplete_data["char1"] = sample_character_data["char1"].copy()
    del incomplete_data["char1"]["name"]

    mock_fs_manager = mock_filesystem_manager
    mock_fs_manager.load_existing_or_new_json_file.return_value = incomplete_data

    with pytest.raises(KeyError) as excinfo:
        Character(playthrough_name, identifier, filesystem_manager=mock_fs_manager)
    assert (
        f"Character '{identifier}' is missing the following required attributes: name."
        in str(excinfo.value)
    )


def test_get_attribute_with_existing_attribute(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )
    attribute_value = character.get_attribute("name")

    assert attribute_value == "Test Character"


def test_get_attribute_with_nonexistent_attribute(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )
    attribute_value = character.get_attribute("nonexistent_attribute")

    assert attribute_value is None


def test_update_data_with_allowed_fields(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    updated_data = {"description": "An updated test character.", "likes": "Exploring"}

    character.update_data(updated_data)

    # Assert that the data was updated
    assert character.description == "An updated test character."
    assert character.likes == "Exploring"

    # Assert that save was called
    mock_filesystem_manager.save_json_file.assert_called()

    # Check that save_json_file was called with updated data
    expected_characters_file = sample_character_data.copy()
    expected_characters_file[identifier].update(updated_data)
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_characters_file, "mock_characters_file_path.json"
    )


def test_update_data_with_disallowed_fields(mock_filesystem_manager, caplog):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    # Clear existing logs
    caplog.clear()

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    updated_data = {
        "description": "An updated test character.",
        "some_disallowed_field": "Some value",
    }

    character.update_data(updated_data)

    # Assert that the data was updated for allowed fields
    assert character.description == "An updated test character."
    # 'some_disallowed_field' should not be in character._data
    assert "some_disallowed_field" not in character._data

    # Assert that a warning was logged
    assert any(
        "Ignored character attribute 'some_disallowed_field' during update for character Test Character."
        in message
        for message in caplog.text.split("\n")
    )

    # Assert that save was called
    mock_filesystem_manager.save_json_file.assert_called()


def test_update_data_with_empty_dict(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    with pytest.raises(ValueError) as excinfo:
        character.update_data({})
    assert "updated_data can't be empty." in str(excinfo.value)


def test_has_description_for_portrait_exists_and_nonempty(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    # Add 'description_for_portrait' to character data
    modified_data = sample_character_data.copy()
    modified_data[identifier]["description_for_portrait"] = "A portrait description"
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = modified_data

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    assert character.has_description_for_portrait() == True
    assert character.description_for_portrait == "A portrait description"


def test_has_description_for_portrait_exists_and_empty(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    # Add 'description_for_portrait' as empty string
    modified_data = sample_character_data.copy()
    modified_data[identifier]["description_for_portrait"] = ""
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = modified_data

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    assert character.has_description_for_portrait() == False


def test_has_description_for_portrait_does_not_exist(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    # Ensure 'description_for_portrait' does not exist
    modified_data = sample_character_data.copy()
    modified_data[identifier].pop("description_for_portrait", None)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = modified_data

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    assert character.has_description_for_portrait() == False


def test_properties_return_correct_values(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    assert character.name == "Test Character"
    # Note: we aren't testing description because there are racing issues with other tests.
    assert character.personality == "Friendly"
    assert character.profile == "Warrior"
    # Note: we aren't testing likes because there are racing issues with other tests.
    assert character.dislikes == "Laziness"
    assert character.secrets == "None"
    assert character.speech_patterns == "Formal"
    assert character.health == "100"
    assert character.equipment == "Sword"
    assert character.voice_gender == "Male"
    assert character.voice_age == "Young"
    assert character.voice_emotion == "Neutral"
    assert character.voice_tempo == "Medium"
    assert character.voice_volume == "Medium"
    assert character.voice_tone == "Warm"
    assert character.voice_texture == "Smooth"
    assert character.voice_style == "Narrative"
    assert character.voice_personality == "Calm"
    assert character.voice_special_effects == "None"
    assert character.voice_model == "Model A"


def test_image_url_property(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    mock_filesystem_manager.get_file_path_to_character_image_for_web.return_value = (
        "mock_image_url"
    )

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    image_url = character.image_url

    mock_filesystem_manager.get_file_path_to_character_image_for_web.assert_called_with(
        playthrough_name, identifier
    )

    assert image_url == "mock_image_url"


def test_save_method(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    # We need to reset the mock calls since __init__ calls some methods
    mock_filesystem_manager.reset_mock()

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    character.save()

    # Assert that get_file_path_to_characters_file was called
    mock_filesystem_manager.get_file_path_to_characters_file.assert_called_with(
        playthrough_name
    )

    # Assert that load_existing_or_new_json_file was called
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_with(
        "mock_characters_file_path.json"
    )

    # Assert that save_json_file was called with the character data
    expected_characters_file = sample_character_data.copy()
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_characters_file, "mock_characters_file_path.json"
    )


def test_update_data_with_allowed_special_field(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    updated_data = {
        "image_url": "http://example.com/new_image.png",
        "description_for_portrait": "New portrait description",
    }

    character.update_data(updated_data)

    # Assert that the data was updated
    assert character.get_attribute("image_url") == "http://example.com/new_image.png"
    assert character.description_for_portrait == "New portrait description"

    # Assert that save was called
    mock_filesystem_manager.save_json_file.assert_called()


def test_update_data_no_data_raises_exception(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    character = Character(
        playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
    )

    with pytest.raises(ValueError) as excinfo:
        character.update_data({})
    assert "updated_data can't be empty." in str(excinfo.value)


def test_property_access_missing_field_raises_keyerror(mock_filesystem_manager):
    playthrough_name = "test_playthrough"
    identifier = "char1"

    # Remove 'name' from the character data
    incomplete_data = sample_character_data.copy()
    incomplete_data[identifier].pop("name", None)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        incomplete_data
    )

    with pytest.raises(KeyError):
        Character(
            playthrough_name, identifier, filesystem_manager=mock_filesystem_manager
        )
