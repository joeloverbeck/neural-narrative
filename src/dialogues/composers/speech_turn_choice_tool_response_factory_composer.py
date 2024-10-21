from src.base.required_string import RequiredString
from src.dialogues.factories.character_choice_dialogue_initial_prompting_messages_provider_factory import (
    CharacterChoiceDialogueInitialPromptingMessagesProviderFactory,
)
from src.dialogues.factories.character_choice_dialogue_system_content_for_prompt_provider_factory import (
    CharacterChoiceDialogueSystemContentForPromptProviderFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.strategies.prevent_llm_from_choosing_player_as_next_speaker_strategy import (
    PreventLlmFromChoosingPlayerAsNextSpeakerStrategy,
)
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.factories.character_choice_dialogue_llm_content_provider_factory import (
    CharacterChoiceDialogueLlmContentProviderFactory,
)
from src.prompting.factories.handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory import (
    HandleParsedToolResponseForDialogueCharacterChoiceStrategyFactory,
)
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import (
    SpeechTurnChoiceToolResponseProviderFactory,
)
from src.prompting.factories.tool_response_parsing_provider_factory import (
    ToolResponseParsingProviderFactory,
)


class SpeechTurnChoiceToolResponseFactoryComposer:
    def __init__(
        self,
        playthrough_name: RequiredString,
        player_identifier: RequiredString,
        participants: Participants,
        llm_client: LlmClient,
        model: RequiredString,
    ):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._llm_client = llm_client
        self._model = model

    def compose(self) -> SpeechTurnChoiceToolResponseProviderFactory:
        character_choice_dialogue_system_content_for_prompt_provider_factory = (
            CharacterChoiceDialogueSystemContentForPromptProviderFactory(
                self._player_identifier
            )
        )

        character_choice_dialogue_initial_prompting_messages_provider_factory = (
            CharacterChoiceDialogueInitialPromptingMessagesProviderFactory(
                character_choice_dialogue_system_content_for_prompt_provider_factory
            )
        )

        llm_content_provider_factory = CharacterChoiceDialogueLlmContentProviderFactory(
            self._llm_client, self._model
        )

        tool_response_parsing_provider_factory = ToolResponseParsingProviderFactory()

        prevent_llm_from_choosing_player_as_next_speaker_strategy = (
            PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
                self._playthrough_name, self._participants
            )
        )

        handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory = (
            HandleParsedToolResponseForDialogueCharacterChoiceStrategyFactory(
                self._playthrough_name,
                self._participants,
                tool_response_parsing_provider_factory,
                prevent_llm_from_choosing_player_as_next_speaker_strategy,
            )
        )

        return SpeechTurnChoiceToolResponseProviderFactory(
            self._playthrough_name,
            self._participants,
            character_choice_dialogue_initial_prompting_messages_provider_factory,
            llm_content_provider_factory,
            handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory,
        )
