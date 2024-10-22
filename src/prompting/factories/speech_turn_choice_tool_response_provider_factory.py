from src.dialogues.factories.character_choice_dialogue_initial_prompting_messages_provider_factory import \
    CharacterChoiceDialogueInitialPromptingMessagesProviderFactory
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.factories.character_choice_dialogue_llm_content_provider_factory import \
    CharacterChoiceDialogueLlmContentProviderFactory
from src.prompting.factories.handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory import \
    HandleParsedToolResponseForDialogueCharacterChoiceStrategyFactory
from src.prompting.providers.speech_turn_tool_response_provider import SpeechTurnChoiceToolResponseProvider


class SpeechTurnChoiceToolResponseProviderFactory:

    def __init__(self, playthrough_name: str, participants: Participants,
                 character_choice_dialogue_initial_prompting_messages_provider_factory:
                 CharacterChoiceDialogueInitialPromptingMessagesProviderFactory,
                 character_choice_dialogue_llm_content_provider_factory:
                 CharacterChoiceDialogueLlmContentProviderFactory,
                 handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory
                 : HandleParsedToolResponseForDialogueCharacterChoiceStrategyFactory):
        self._playthrough_name = playthrough_name
        self._participants = participants
        (self.
         _character_choice_dialogue_initial_prompting_messages_provider_factory
         ) = (
            character_choice_dialogue_initial_prompting_messages_provider_factory
        )
        self._character_choice_dialogue_llm_content_provider_factory = (
            character_choice_dialogue_llm_content_provider_factory)
        (self.
         _handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory
         ) = (
            handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory
        )

    def create_speech_turn_choice_tool_response_provider(self,
                                                         transcription: Transcription) -> SpeechTurnChoiceToolResponseProvider:
        return SpeechTurnChoiceToolResponseProvider(self._playthrough_name,
                                                    self._participants, transcription, self.
                                                    _character_choice_dialogue_initial_prompting_messages_provider_factory
                                                    , self._character_choice_dialogue_llm_content_provider_factory,
                                                    self.
                                                    _handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory
                                                    )
