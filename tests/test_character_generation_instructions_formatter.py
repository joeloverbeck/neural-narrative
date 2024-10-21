from unittest.mock import Mock

import pytest

from src.base.required_string import RequiredString
from src.characters.characters_manager import CharactersManager
from src.prompting.formatters.character_generation_instructions_formatter import (
    CharacterGenerationInstructionsFormatter,
)


def test_init_with_valid_parameters():
    playthrough_name = RequiredString("Adventure")
    places_descriptions = RequiredString("A dark forest.")
    templates = {
        "character_generation_instructions": "Instructions with {places_descriptions} and {prohibited_names}"
    }
    characters_manager = Mock(spec=CharactersManager)
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    assert formatter._places_descriptions == places_descriptions
    assert formatter._templates == templates
    assert formatter._characters_manager == characters_manager


def test_format_returns_correct_instructions():
    playthrough_name = RequiredString("Quest")
    places_descriptions = RequiredString("an ancient ruin")
    templates = {
        "character_generation_instructions": "Explore {places_descriptions}. Avoid {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = ["Alice", "Bob"]
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    expected_instructions = "Explore an ancient ruin. Avoid ['Alice', 'Bob']."
    formatted_instructions = formatter.format()
    assert isinstance(formatted_instructions, RequiredString)
    assert formatted_instructions.value == expected_instructions


def test_format_raises_key_error_when_template_missing():
    playthrough_name = RequiredString("Mystery")
    places_descriptions = RequiredString("a haunted house")
    templates = {}  # Empty templates dict
    characters_manager = Mock(spec=CharactersManager)
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    with pytest.raises(KeyError):
        formatter.format()


def test_format_with_empty_prohibited_names():
    playthrough_name = RequiredString("Journey")
    places_descriptions = RequiredString("a distant galaxy")
    templates = {
        "character_generation_instructions": "Travel through {places_descriptions}. Watch out for {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = []
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    expected_instructions = "Travel through a distant galaxy. Watch out for []."
    formatted_instructions = formatter.format()
    assert formatted_instructions.value == expected_instructions


def test_format_raises_key_error_on_template_formatting_error():
    playthrough_name = RequiredString("Odyssey")
    places_descriptions = RequiredString("a mythical land")
    templates = {
        "character_generation_instructions": "Discover {places_descriptions}. Beware of {unknown_parameter}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = ["Cyclops"]
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    with pytest.raises(KeyError):
        formatter.format()


def test_format_with_unicode_characters():
    playthrough_name = RequiredString("Saga")
    places_descriptions = RequiredString("a realm of dragons 🐉 and magic ✨")
    templates = {
        "character_generation_instructions": "Enter {places_descriptions}. Keep away from {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = ["Smaug", "Merlin"]
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    expected_instructions = (
        "Enter a realm of dragons 🐉 and magic ✨. Keep away from ['Smaug', 'Merlin']."
    )
    formatted_instructions = formatter.format()
    assert formatted_instructions.value == expected_instructions


def test_format_with_prohibited_names_none():
    playthrough_name = RequiredString("Expedition")
    places_descriptions = RequiredString("the uncharted waters")
    templates = {
        "character_generation_instructions": "Navigate {places_descriptions}. Avoid {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = None
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    expected_instructions = "Navigate the uncharted waters. Avoid None."
    formatted_instructions = formatter.format()
    assert formatted_instructions.value == expected_instructions


def test_format_when_get_all_character_names_raises_exception():
    playthrough_name = RequiredString("Voyage")
    places_descriptions = RequiredString("an endless desert")
    templates = {
        "character_generation_instructions": "Survive {places_descriptions}. Beware of {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.side_effect = Exception(
        "Data retrieval failed"
    )
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    with pytest.raises(Exception, match="Data retrieval failed"):
        formatter.format()


def test_init_with_empty_playthrough_name_raises_exception():
    with pytest.raises(ValueError, match="value can't be empty."):
        playthrough_name = RequiredString("")
        places_descriptions = RequiredString("a mysterious cave")
        templates = {}
        CharacterGenerationInstructionsFormatter(
            playthrough_name, places_descriptions, templates
        )


def test_init_with_non_string_playthrough_name_raises_exception():
    with pytest.raises(TypeError, match="value must be a string"):
        playthrough_name = RequiredString(123)
        places_descriptions = RequiredString("a mysterious cave")
        templates = {}
        CharacterGenerationInstructionsFormatter(
            playthrough_name, places_descriptions, templates
        )


def test_format_with_additional_template_parameters():
    playthrough_name = RequiredString("Quest")
    places_descriptions = RequiredString("an enchanted forest")
    templates = {
        "character_generation_instructions": "Explore {places_descriptions}. Use {tools}. Avoid {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = ["Goblin"]
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    # Since 'tools' is not provided, this should raise a KeyError
    with pytest.raises(KeyError):
        formatter.format()


def test_format_with_special_characters_in_prohibited_names():
    playthrough_name = RequiredString("Adventure")
    places_descriptions = RequiredString("a vast ocean")
    templates = {
        "character_generation_instructions": "Sail across {places_descriptions}. Beware of {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = [
        "Kraken",
        "Davy Jones' Locker",
    ]
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    expected_instructions = (
        "Sail across a vast ocean. Beware of ['Kraken', \"Davy Jones' Locker\"]."
    )
    formatted_instructions = formatter.format()
    assert formatted_instructions.value == expected_instructions


def test_format_with_large_prohibited_names_list():
    playthrough_name = RequiredString("Epic")
    places_descriptions = RequiredString("a grand city")
    templates = {
        "character_generation_instructions": "Enter {places_descriptions}. Do not mention {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = [
        f"Character_{i}" for i in range(100)
    ]
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    prohibited_names_list = characters_manager.get_all_character_names.return_value
    expected_instructions = (
        f"Enter a grand city. Do not mention {prohibited_names_list}."
    )
    formatted_instructions = formatter.format()
    assert formatted_instructions.value == expected_instructions


def test_format_with_non_string_prohibited_names():
    playthrough_name = RequiredString("Mystery")
    places_descriptions = RequiredString("an abandoned castle")
    templates = {
        "character_generation_instructions": "Investigate {places_descriptions}. Avoid {prohibited_names}."
    }
    characters_manager = Mock(spec=CharactersManager)
    characters_manager.get_all_character_names.return_value = ["Ghost", 123, None]
    formatter = CharacterGenerationInstructionsFormatter(
        playthrough_name,
        places_descriptions,
        templates,
        characters_manager,
    )
    expected_instructions = (
        "Investigate an abandoned castle. Avoid ['Ghost', 123, None]."
    )
    formatted_instructions = formatter.format()
    assert formatted_instructions.value == expected_instructions
