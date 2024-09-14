from typing import List

from src.dialogues.factories.determine_system_message_for_speech_turn_strategy_factory import \
    DetermineSystemMessageForSpeechTurnStrategyFactory
from src.dialogues.factories.determine_user_messages_for_speech_turn_strategy_factory import \
    DetermineUserMessagesForSpeechTurnStrategyFactory
from src.dialogues.factories.dialogue_initial_prompting_messages_provider_factory import \
    DialogueInitialPromptingMessagesProviderFactory
from src.dialogues.factories.prompt_formatter_for_dialogue_strategy_factory import \
    PromptFormatterForDialogueStrategyFactory
from src.dialogues.factories.speech_turn_dialogue_system_content_for_prompt_provider_factory import \
    SpeechTurnDialogueSystemContentForPromptProviderFactory
from src.dialogues.factories.speech_turn_produce_messages_to_prompt_llm_command_factory import \
    SpeechTurnProduceMessagesToPromptLlmCommandFactory
from src.maps.factories.concrete_full_place_data_factory import ConcreteFullPlaceDataFactory
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import \
    SpeechTurnChoiceToolResponseProviderFactory


class SpeechTurnProduceMessagesToPromptLlmCommandFactoryComposer:
    def __init__(self, playthrough_name: str, player_identifier: str, participants: List[str],
                 speech_turn_choice_tool_response_provider_factory: SpeechTurnChoiceToolResponseProviderFactory):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not player_identifier:
            raise ValueError("player identifier can't be empty.")
        if not len(participants) >= 2:
            raise ValueError("There should be at least two participants in the dialogue.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._speech_turn_choice_tool_response_provider_factory = speech_turn_choice_tool_response_provider_factory

    def compose(self) -> SpeechTurnProduceMessagesToPromptLlmCommandFactory:
        full_place_data_factory = ConcreteFullPlaceDataFactory(self._playthrough_name)

        prompt_formatter_for_dialogue_strategy_factory = PromptFormatterForDialogueStrategyFactory(
            self._playthrough_name,
            full_place_data_factory)

        speech_turn_dialogue_system_content_for_prompt_provider_factory = SpeechTurnDialogueSystemContentForPromptProviderFactory(
            prompt_formatter_for_dialogue_strategy_factory)

        dialogue_initial_prompting_messages_provider_factory = DialogueInitialPromptingMessagesProviderFactory(
            self._playthrough_name, self._participants, speech_turn_dialogue_system_content_for_prompt_provider_factory)

        determine_system_message_for_speech_turn_strategy_factory = DetermineSystemMessageForSpeechTurnStrategyFactory(
            dialogue_initial_prompting_messages_provider_factory)

        determine_user_messages_for_speech_turn_strategy_factory = DetermineUserMessagesForSpeechTurnStrategyFactory(
            self._playthrough_name, self._player_identifier)

        return SpeechTurnProduceMessagesToPromptLlmCommandFactory(
            self._speech_turn_choice_tool_response_provider_factory,
            determine_system_message_for_speech_turn_strategy_factory,
            determine_user_messages_for_speech_turn_strategy_factory)
