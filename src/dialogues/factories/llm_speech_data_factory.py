from typing import List, Optional, Any

from src.abstracts.observer import Observer
from src.abstracts.subject import Subject
from src.characters.characters import load_character_data, load_character_memories
from src.constants import HERMES_405B
from src.dialogues.abstracts.abstract_factories import SpeechDataFactory
from src.dialogues.abstracts.factory_products import SpeechDataProduct, PlayerInputProduct
from src.dialogues.dialogues import gather_participant_data
from src.dialogues.factories.dialogue_initial_prompting_messages_factory import DialogueInitialPromptingMessagesFactory
from src.dialogues.products.concrete_speech_data_product import ConcreteSpeechDataProduct
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory
from src.prompting.factories.speech_tool_response_data_extraction_factory import SpeechToolResponseDataExtractionFactory


class LlmSpeechDataFactory(SpeechDataFactory, Subject):

    def __init__(self, client, playthrough_name: str, player_identifier: Optional[int], participants: List[int],
                 player_input_product: PlayerInputProduct, previous_messages: List[dict],
                 speech_turn_data: dict[str, str],
                 dialogue: List[dict[Any, str]]):
        assert client
        assert playthrough_name
        assert len(participants) >= 2
        assert player_input_product
        assert speech_turn_data
        assert "identifier" in speech_turn_data

        self._client = client
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._player_input_product = player_input_product
        self._previous_messages = previous_messages
        self._speech_turn_data = speech_turn_data
        self._dialogue = dialogue

        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def _append_message_to_messages(self, message: dict, current_turn_messages: List[dict]):
        current_turn_messages.append(message)
        self._previous_messages.append(message)

    def create_speech_data(self) -> SpeechDataProduct:
        # The next AI character should get its own system message (that includes peculiarities for that character),
        # as well as all the non system messages that came up to that point.
        dialogue_initial_prompting_messages_product = DialogueInitialPromptingMessagesFactory(
            gather_participant_data(self._playthrough_name, self._participants),
            character_data=load_character_data(self._playthrough_name,
                                               int(self._speech_turn_data["identifier"])),
            memories=load_character_memories(self._playthrough_name,
                                             int(self._speech_turn_data[
                                                     "identifier"]))).create_initial_prompting_messages()

        current_turn_messages = dialogue_initial_prompting_messages_product.get()

        # I have to append the previous messages, if any.
        if self._previous_messages:
            current_turn_messages.extend(self._previous_messages)

        # In case there's no player present, or has remained silent, a 'user' prompt
        # should be appended to the ongoing messages. Otherwise, the LLM won't answer anything.
        if not self._player_identifier or self._player_input_product.is_silent():
            # Should prompt the LLM to speak given the chosen next character.
            self._append_message_to_messages(
                {"role": "user", "content": f"Produce {self._speech_turn_data["name"]}'s speech."},
                current_turn_messages)

        llm_content_product = OpenAiLlmContentFactory(client=self._client, model=HERMES_405B,
                                                      messages=current_turn_messages).generate_content()
        if not llm_content_product.is_valid():
            return ConcreteSpeechDataProduct({}, is_valid=False,
                                             error=f"LLM failed to produce a response: {llm_content_product.get_error()}")

        self._append_message_to_messages({"role": "assistant", "content": llm_content_product.get()},
                                         current_turn_messages)

        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            raise ValueError(
                f"Was unable to parse the tool response: {tool_response_parsing_product.get()}\nLLM response content: {llm_content_product.get()}")

        return ConcreteSpeechDataProduct(SpeechToolResponseDataExtractionFactory(
            tool_response_parsing_product.get()).extract_data().get(), is_valid=True)
