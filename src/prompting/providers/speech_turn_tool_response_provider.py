from src.dialogues.factories.character_choice_dialogue_initial_prompting_messages_provider_factory import \
    CharacterChoiceDialogueInitialPromptingMessagesProviderFactory
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.abstract_factories import ToolResponseProvider
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.character_choice_dialogue_llm_content_provider_factory import \
    CharacterChoiceDialogueLlmContentProviderFactory
from src.prompting.factories.handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory import \
    HandleParsedToolResponseForDialogueCharacterChoiceStrategyFactory
from src.prompting.products.concrete_llm_tool_response_product import ConcreteLlmToolResponseProduct


class SpeechTurnChoiceToolResponseProvider(ToolResponseProvider):
    def __init__(self, participants: Participants, transcription: Transcription,
                 character_choice_dialogue_initial_prompting_messages_provider_factory: CharacterChoiceDialogueInitialPromptingMessagesProviderFactory,
                 llm_content_provider_factory: CharacterChoiceDialogueLlmContentProviderFactory,
                 handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory: HandleParsedToolResponseForDialogueCharacterChoiceStrategyFactory):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._participants = participants
        self._transcription = transcription
        self._character_choice_dialogue_initial_prompting_messages_provider_factory = character_choice_dialogue_initial_prompting_messages_provider_factory
        self._llm_content_provider_factory = llm_content_provider_factory
        self._handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory = handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory

    def create_llm_response(self) -> LlmToolResponseProduct:
        character_choice_dialogue_initial_prompting_messages_product = self._character_choice_dialogue_initial_prompting_messages_provider_factory.create_character_choice_dialogue_initial_prompting_messages_provider(
            self._participants, self._transcription).create_initial_prompting_messages()

        llm_content_product = self._llm_content_provider_factory.create_llm_content_provider_factory(
            character_choice_dialogue_initial_prompting_messages_product).generate_content()

        if not llm_content_product.is_valid():
            return ConcreteLlmToolResponseProduct(llm_response={}, is_valid=False,
                                                  error=f"LLM failed to produce a response: {llm_content_product.get_error()}")

        return self._handle_parsed_tool_response_for_dialogue_character_choice_strategy_factory.create_handle_parsed_tool_response_for_dialogue_character_choice_strategy().handle_parsed_tool_response(
            llm_content_product)
