from typing import List, Optional, Any

from src.constants import HERMES_405B
from src.dialogues.dialogues import gather_participant_data
from src.dialogues.factories.character_choice_dialogue_initial_prompting_messages_factory import \
    CharacterChoiceDialogueInitialPromptingMessagesFactory
from src.prompting.abstracts.abstract_factories import ToolResponseFactory
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory
from src.prompting.products.concrete_llm_tool_response_product import ConcreteLlmToolResponseProduct


class SpeechTurnToolResponseFactory(ToolResponseFactory):
    def __init__(self, client, playthrough_name: str, player_identifier: Optional[int], participants: List[int],
                 dialogue: List[dict[Any, str]]):
        assert client
        assert playthrough_name
        assert len(participants) >= 2

        self._client = client
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._dialogue = dialogue

    def create_llm_response(self) -> LlmToolResponseProduct:
        # "participants" here should be a List[dict] containing the identifiers and names
        participants = gather_participant_data(self._playthrough_name, self._participants)

        character_choice_dialogue_initial_prompting_messages_product = CharacterChoiceDialogueInitialPromptingMessagesFactory(
            participants, self._player_identifier, self._dialogue).create_initial_prompting_messages()

        speech_turn_messages = character_choice_dialogue_initial_prompting_messages_product.get()
        speech_turn_messages.append({"role": "user", "content": "Choose who will speak next."})

        llm_content_product = OpenAiLlmContentFactory(client=self._client, model=HERMES_405B,
                                                      messages=speech_turn_messages).generate_content()

        if not llm_content_product.is_valid():
            return ConcreteLlmToolResponseProduct(llm_response={}, is_valid=False,
                                                  error=f"LLM failed to produce a response: {llm_content_product.get_error()}")

        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        assert tool_response_parsing_product.is_valid()

        if "identifier" not in tool_response_parsing_product.get()["arguments"]:
            return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=False,
                                                  error=f"The LLM didn't produce the identifier of the character who ought to speak next: {tool_response_parsing_product.get()}")

        return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get()["arguments"], is_valid=True)
