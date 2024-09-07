from typing import List

from src.constants import DIALOGUE_PROMPT_FILE, SPEECH_GENERATOR_TOOL_FILE
from src.dialogues.abstracts.abstract_factories import InitialPromptingMessagesFactory
from src.dialogues.abstracts.factory_products import InitialPromptingMessagesProduct
from src.prompting.products.concrete_initial_prompting_messages_product import ConcreteInitialPromptingMessagesProduct
from src.prompting.prompting import create_system_content_for_dialogue_prompt


class DialogueInitialPromptingMessagesFactory(InitialPromptingMessagesFactory):
    def __init__(self, participants: List[dict], character_data: dict, memories: str):
        assert len(participants) >= 2
        assert character_data

        self._participants = participants
        self._character_data = character_data
        self._memories = memories

    def create_initial_prompting_messages(self) -> InitialPromptingMessagesProduct:
        other_character_name: str = "[CHARACTER]"

        for character in self._participants:
            if character["name"] != self._character_data["name"]:
                other_character_name = character["name"]
                break

        return ConcreteInitialPromptingMessagesProduct([{"role": "system",
                                                         "content": create_system_content_for_dialogue_prompt(
                                                             self._participants,
                                                             self._character_data, self._memories,
                                                             DIALOGUE_PROMPT_FILE,
                                                             SPEECH_GENERATOR_TOOL_FILE)},
                                                        {"role": "user",
                                                         "content": f"Here's an example: {other_character_name}: What's up?"},
                                                        {"role": "assistant",
                                                         "content": f"<function=generate_speech>{{\"name\": \"{self._character_data["name"]}\", \"speech\": \"What's up with you?\", \"narration_text\": \"{self._character_data["name"]} looks curiously.\" }}</function>"}])
