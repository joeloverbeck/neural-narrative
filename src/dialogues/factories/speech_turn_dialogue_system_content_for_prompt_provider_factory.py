from typing import List

from src.constants import SPEECH_GENERATOR_TOOL_FILE
from src.dialogues.factories.prompt_formatter_for_dialogue_strategy_factory import \
    PromptFormatterForDialogueStrategyFactory
from src.dialogues.providers.speech_turn_dialogue_system_content_for_prompt_provider import \
    SpeechTurnDialogueSystemContentForPromptProvider


class SpeechTurnDialogueSystemContentForPromptProviderFactory:
    def __init__(self, prompt_formatter_for_dialogue_strategy_factory: PromptFormatterForDialogueStrategyFactory

                 ):
        self._prompt_formatter_for_dialogue_strategy_factory = prompt_formatter_for_dialogue_strategy_factory

    def create_speech_turn_dialogue_system_content_for_prompt_provider(
            self, participants_data: List[dict], character_data: dict,
            memories: str) -> SpeechTurnDialogueSystemContentForPromptProvider:
        return SpeechTurnDialogueSystemContentForPromptProvider(
            character_data,
            SPEECH_GENERATOR_TOOL_FILE,
            self._prompt_formatter_for_dialogue_strategy_factory.create_prompt_formatter_for_dialogue_strategy_factory(
                participants_data,
                character_data, memories))
