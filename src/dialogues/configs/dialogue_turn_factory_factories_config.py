from dataclasses import dataclass

from src.characters.factories.character_factory import CharacterFactory
from src.dialogues.factories.create_speech_turn_data_command_factory import (
    CreateSpeechTurnDataCommandFactory,
)
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import (
    SpeechTurnChoiceToolResponseProviderFactory,
)


@dataclass
class DialogueTurnFactoryFactoriesConfig:
    character_factory: CharacterFactory
    speech_turn_choice_tool_response_provider_factory: (
        SpeechTurnChoiceToolResponseProviderFactory
    )
    create_speech_turn_data_command_factory: CreateSpeechTurnDataCommandFactory
