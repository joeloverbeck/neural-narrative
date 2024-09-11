from typing import List

from src.constants import DIALOGUE_PROMPT_FILE, SPEECH_GENERATOR_TOOL_FILE
from src.dialogues.abstracts.abstract_factories import InitialPromptingMessagesFactory
from src.dialogues.abstracts.factory_products import InitialPromptingMessagesProduct
from src.dialogues.factories.ConcretePlaceDataForDialoguePromptFactory import ConcretePlaceDataForDialoguePromptFactory
from src.dialogues.factories.speech_turn_dialogue_system_content_for_prompt_factory import \
    SpeechTurnDialogueSystemContentForPromptFactory
from src.dialogues.strategies.concrete_prompt_formatter_for_dialogue_strategy import \
    ConcretePromptFormatterForDialogueStrategy
from src.maps.factories.concrete_current_location_data_factory import ConcreteCurrentLocationDataFactory
from src.prompting.products.concrete_initial_prompting_messages_product import ConcreteInitialPromptingMessagesProduct


class DialogueInitialPromptingMessagesFactory(InitialPromptingMessagesFactory):
    def __init__(self, playthrough_name: str, participants: List[dict],
                 character_data: dict,
                 memories: str):
        assert playthrough_name
        assert len(participants) >= 2
        assert character_data

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._character_data = character_data
        self._memories = memories

    def create_initial_prompting_messages(self) -> InitialPromptingMessagesProduct:
        other_character_name: str = "[CHARACTER]"

        for character in self._participants:
            if character["name"] != self._character_data["name"]:
                other_character_name = character["name"]
                break

        system_content_for_prompt_product = SpeechTurnDialogueSystemContentForPromptFactory(
            self._character_data,
            SPEECH_GENERATOR_TOOL_FILE,
            ConcretePromptFormatterForDialogueStrategy(self._playthrough_name, self._participants,
                                                       self._character_data, self._memories,
                                                       DIALOGUE_PROMPT_FILE,
                                                       ConcretePlaceDataForDialoguePromptFactory(self._playthrough_name,
                                                                                                 ConcreteCurrentLocationDataFactory(
                                                                                                     self._playthrough_name)))).create_system_content_for_prompt()

        if not system_content_for_prompt_product.is_valid():
            raise ValueError(
                f"Failed to produce the system content for the speech turn: {system_content_for_prompt_product.get_error()}")

        return ConcreteInitialPromptingMessagesProduct([{"role": "system",
                                                         "content": system_content_for_prompt_product.get()},
                                                        {"role": "user",
                                                         "content": f"Here's an example: {other_character_name}: What's up?"},
                                                        {"role": "assistant",
                                                         "content": f"<function=generate_speech>{{\"name\": \"{self._character_data["name"]}\", \"speech\": \"What's up with you?\", \"narration_text\": \"{self._character_data["name"]} looks curiously.\" }}</function>"},
                                                        {"role": "user",
                                                         "content": f"Here's an second: {other_character_name}: Hey!"},
                                                        {"role": "assistant",
                                                         "content": f"<function=generate_speech>{{\"name\": \"{self._character_data["name"]}\", \"speech\": \"What do you want?\", \"narration_text\": \"{self._character_data["name"]} looks curiously.\" }}</function>"}])
