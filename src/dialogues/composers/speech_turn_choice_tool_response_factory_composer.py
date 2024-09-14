from typing import List

from src.dialogues.factories.character_choice_dialogue_initial_prompting_messages_provider_factory import \
    CharacterChoiceDialogueInitialPromptingMessagesProviderFactory
from src.dialogues.factories.character_choice_dialogue_system_content_for_prompt_provider_factory import \
    CharacterChoiceDialogueSystemContentForPromptProviderFactory
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.factories.character_choice_dialogue_llm_content_provider_factory import \
    CharacterChoiceDialogueLlmContentProviderFactory
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import \
    SpeechTurnChoiceToolResponseProviderFactory
from src.prompting.factories.tool_response_parsing_provider_factory import ToolResponseParsingProviderFactory


class SpeechTurnChoiceToolResponseFactoryComposer:
    def __init__(self, playthrough_name: str, player_identifier: str, participants: List[str], llm_client: LlmClient,
                 model: str):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not player_identifier:
            raise ValueError("player identifier can't be empty.")
        if not len(participants) >= 2:
            raise ValueError("There should be at least two participants in the dialogue.")
        if not model:
            raise ValueError("model can't be empty.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._llm_client = llm_client
        self._model = model

    def compose(self) -> SpeechTurnChoiceToolResponseProviderFactory:
        character_choice_dialogue_system_content_for_prompt_provider_factory = CharacterChoiceDialogueSystemContentForPromptProviderFactory(
            self._player_identifier)

        character_choice_dialogue_initial_prompting_messages_provider_factory = CharacterChoiceDialogueInitialPromptingMessagesProviderFactory(
            character_choice_dialogue_system_content_for_prompt_provider_factory)

        llm_content_provider_factory = CharacterChoiceDialogueLlmContentProviderFactory(self._llm_client, self._model)

        tool_response_parsing_provider_factory = ToolResponseParsingProviderFactory()

        return SpeechTurnChoiceToolResponseProviderFactory(self._playthrough_name,
                                                           self._participants,
                                                           character_choice_dialogue_initial_prompting_messages_provider_factory,
                                                           llm_content_provider_factory,
                                                           tool_response_parsing_provider_factory)