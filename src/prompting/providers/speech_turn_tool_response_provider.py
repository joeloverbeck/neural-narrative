from src.dialogues.factories.character_choice_dialogue_initial_prompting_messages_provider_factory import \
    CharacterChoiceDialogueInitialPromptingMessagesProviderFactory
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.abstract_factories import ToolResponseProvider
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.character_choice_dialogue_llm_content_provider_factory import \
    CharacterChoiceDialogueLlmContentProviderFactory
from src.prompting.factories.tool_response_parsing_provider_factory import ToolResponseParsingProviderFactory
from src.prompting.products.concrete_llm_tool_response_product import ConcreteLlmToolResponseProduct


class SpeechTurnChoiceToolResponseProvider(ToolResponseProvider):
    def __init__(self, playthrough_name: str, participants: Participants, transcription: Transcription,
                 character_choice_dialogue_initial_prompting_messages_provider_factory: CharacterChoiceDialogueInitialPromptingMessagesProviderFactory,
                 llm_content_provider_factory: CharacterChoiceDialogueLlmContentProviderFactory,
                 tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._transcription = transcription
        self._character_choice_dialogue_initial_prompting_messages_provider_factory = character_choice_dialogue_initial_prompting_messages_provider_factory
        self._llm_content_provider_factory = llm_content_provider_factory
        self._tool_response_parsing_provider_factory = tool_response_parsing_provider_factory

    def create_llm_response(self) -> LlmToolResponseProduct:
        character_choice_dialogue_initial_prompting_messages_product = self._character_choice_dialogue_initial_prompting_messages_provider_factory.create_character_choice_dialogue_initial_prompting_messages_provider(
            self._participants, self._transcription).create_initial_prompting_messages()

        llm_content_product = self._llm_content_provider_factory.create_llm_content_provider_factory(
            character_choice_dialogue_initial_prompting_messages_product).generate_content()

        if not llm_content_product.is_valid():
            return ConcreteLlmToolResponseProduct(llm_response={}, is_valid=False,
                                                  error=f"LLM failed to produce a response: {llm_content_product.get_error()}")

        tool_response_parsing_product = self._tool_response_parsing_provider_factory.create_tool_response_parsing_provider(
            llm_content_product).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=False,
                                                  error=f"Was unable to parse the tool response from the LLM: {tool_response_parsing_product.get_error()}")

        if "identifier" not in tool_response_parsing_product.get()["arguments"]:
            return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=False,
                                                  error=f"The LLM didn't produce the identifier of the character who ought to speak next: {tool_response_parsing_product.get()}")

        return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get()["arguments"], is_valid=True)
