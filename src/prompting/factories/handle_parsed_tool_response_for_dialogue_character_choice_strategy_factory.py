from src.dialogues.participants import Participants
from src.prompting.factories.tool_response_parsing_provider_factory import ToolResponseParsingProviderFactory
from src.prompting.strategies.handle_parsed_tool_response_for_dialogue_character_choice_strategy import \
    HandleParsedToolResponseForDialogueCharacterChoiceStrategy


class HandleParsedToolResponseForDialogueCharacterChoiceStrategyFactory:

    def __init__(self, playthrough_name: str, participants: Participants,
                 tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._tool_response_parsing_provider_factory = tool_response_parsing_provider_factory

    def create_handle_parsed_tool_response_for_dialogue_character_choice_strategy(
            self) -> HandleParsedToolResponseForDialogueCharacterChoiceStrategy:
        return HandleParsedToolResponseForDialogueCharacterChoiceStrategy(self._playthrough_name, self._participants,
                                                                          self._tool_response_parsing_provider_factory)
