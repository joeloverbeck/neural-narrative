from unittest.mock import MagicMock

import pytest

from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.characters.providers.character_generation_tool_response_provider import (
    CharacterGenerationToolResponseProvider,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)


def test_generate_character_command_empty_playthrough_name():
    with pytest.raises(ValueError) as exc_info:
        GenerateCharacterCommand(
            playthrough_name="",
            character_generation_tool_response_provider=MagicMock(
                spec=CharacterGenerationToolResponseProvider
            ),
            store_generate_character_command_factory=MagicMock(
                spec=StoreGeneratedCharacterCommandFactory
            ),
            generate_character_image_command_factory=MagicMock(
                spec=GenerateCharacterImageCommandFactory
            ),
            place_character_at_current_place=True,
        )
    assert "playthrough_name can't be empty." in str(exc_info.value)
