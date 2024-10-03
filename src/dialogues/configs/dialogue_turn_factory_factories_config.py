from dataclasses import dataclass

from src.dialogues.factories.create_speech_turn_data_command_factory import (
    CreateSpeechTurnDataCommandFactory,
)
from src.dialogues.factories.determine_user_messages_for_speech_turn_strategy_factory import (
    DetermineUserMessagesForSpeechTurnStrategyFactory,
)
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import (
    SpeechTurnChoiceToolResponseProviderFactory,
)


@dataclass
class DialogueTurnFactoryFactoriesConfig:
    speech_turn_choice_tool_response_provider_factory: (
        SpeechTurnChoiceToolResponseProviderFactory
    )
    create_speech_turn_data_command_factory: CreateSpeechTurnDataCommandFactory
    determine_user_messages_for_speech_turn_strategy_factory: (
        DetermineUserMessagesForSpeechTurnStrategyFactory
    )
