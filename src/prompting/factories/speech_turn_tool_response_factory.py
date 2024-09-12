from typing import List, Optional

from src.dialogues.dialogues import gather_participant_data
from src.dialogues.factories.character_choice_dialogue_initial_prompting_messages_factory import \
    CharacterChoiceDialogueInitialPromptingMessagesFactory
from src.prompting.abstracts.abstract_factories import ToolResponseFactory
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.factories.concrete_llm_content_factory import ConcreteLlmContentFactory
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.products.concrete_llm_tool_response_product import ConcreteLlmToolResponseProduct


class SpeechTurnChoiceToolResponseFactory(ToolResponseFactory):
    def __init__(self, playthrough_name: str, llm_client: LlmClient, model: str, player_identifier: Optional[int],
                 participants: List[int],
                 dialogue: List[str]):
        assert playthrough_name
        assert llm_client
        assert model
        assert len(participants) >= 2

        self._playthrough_name = playthrough_name
        self._llm_client = llm_client
        self._model = model
        self._player_identifier = player_identifier
        self._participants = participants
        self._dialogue = dialogue

    def create_llm_response(self) -> LlmToolResponseProduct:
        participants = gather_participant_data(self._playthrough_name, self._participants)

        character_choice_dialogue_initial_prompting_messages_product = CharacterChoiceDialogueInitialPromptingMessagesFactory(
            participants, self._player_identifier, self._dialogue).create_initial_prompting_messages()

        llm_content_product = ConcreteLlmContentFactory(model=self._model,
                                                        messages=character_choice_dialogue_initial_prompting_messages_product.get(),
                                                        llm_client=self._llm_client).generate_content()

        if not llm_content_product.is_valid():
            return ConcreteLlmToolResponseProduct(llm_response={}, is_valid=False,
                                                  error=f"LLM failed to produce a response: {llm_content_product.get_error()}")

        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=False,
                                                  error=f"Was unable to parse the tool response from the LLM: {tool_response_parsing_product.get_error()}")

        if "identifier" not in tool_response_parsing_product.get()["arguments"]:
            return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=False,
                                                  error=f"The LLM didn't produce the identifier of the character who ought to speak next: {tool_response_parsing_product.get()}")

        return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get()["arguments"], is_valid=True)
