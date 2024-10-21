from src.base.required_string import RequiredString
from src.dialogues.participants import Participants
from src.dialogues.strategies.prevent_llm_from_choosing_player_as_next_speaker_strategy import (
    PreventLlmFromChoosingPlayerAsNextSpeakerStrategy,
)
from src.prompting.factories.tool_response_parsing_provider_factory import (
    ToolResponseParsingProviderFactory,
)
from src.prompting.strategies.handle_parsed_tool_response_for_dialogue_character_choice_strategy import (
    HandleParsedToolResponseForDialogueCharacterChoiceStrategy,
)


class HandleParsedToolResponseForDialogueCharacterChoiceStrategyFactory:

    def __init__(
        self,
            playthrough_name: RequiredString,
        participants: Participants,
        tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory,
        prevent_llm_from_choosing_player_as_next_speaker_strategy: PreventLlmFromChoosingPlayerAsNextSpeakerStrategy,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._tool_response_parsing_provider_factory = (
            tool_response_parsing_provider_factory
        )
        self._prevent_llm_from_choosing_player_as_next_speaker_strategy = (
            prevent_llm_from_choosing_player_as_next_speaker_strategy
        )

    def create_handle_parsed_tool_response_for_dialogue_character_choice_strategy(
        self,
    ) -> HandleParsedToolResponseForDialogueCharacterChoiceStrategy:
        return HandleParsedToolResponseForDialogueCharacterChoiceStrategy(
            self._playthrough_name,
            self._participants,
            self._tool_response_parsing_provider_factory,
            self._prevent_llm_from_choosing_player_as_next_speaker_strategy,
        )
