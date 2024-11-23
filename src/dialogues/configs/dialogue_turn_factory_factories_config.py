from dataclasses import dataclass

from src.dialogues.factories.create_speech_turn_data_command_factory import (
    CreateSpeechTurnDataCommandFactory,
)


@dataclass
class DialogueTurnFactoryFactoriesConfig:
    create_speech_turn_data_command_factory: CreateSpeechTurnDataCommandFactory
