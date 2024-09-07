from typing import List

from src.characters.characters import load_character_memories, load_character_data
from src.dialogues.abstracts.strategies import DetermineSystemMessageForSpeechTurnStrategy
from src.dialogues.dialogues import gather_participant_data
from src.dialogues.factories.dialogue_initial_prompting_messages_factory import DialogueInitialPromptingMessagesFactory
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class ConcreteDetermineSystemMessageForSpeechTurnStrategy(DetermineSystemMessageForSpeechTurnStrategy):
    def __init__(self, playthrough_name: str, participants: List[int], previous_messages: List[dict]):
        assert playthrough_name
        assert len(participants) >= 2

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._previous_messages = previous_messages

    def do_algorithm(self, speech_turn_tool_response_product: LlmToolResponseProduct):
        # The next AI character should get its own system message (that includes peculiarities for that character).
        dialogue_initial_prompting_messages_product = DialogueInitialPromptingMessagesFactory(
            gather_participant_data(self._playthrough_name, self._participants),
            character_data=load_character_data(self._playthrough_name,
                                               int(speech_turn_tool_response_product.get()["identifier"])),
            memories=load_character_memories(self._playthrough_name,
                                             int(speech_turn_tool_response_product.get()[
                                                     "identifier"]))).create_initial_prompting_messages()

        if self._previous_messages:
            self._previous_messages.pop(0)
            self._previous_messages.insert(0, dialogue_initial_prompting_messages_product.get()[0])
        else:
            self._previous_messages.extend(dialogue_initial_prompting_messages_product.get())
