from types import NoneType
from typing import List, Optional, Any

from src.constants import CHOOSING_SPEECH_TURN_PROMPT_FILE, SPEECH_TURN_TOOL_FILE, TOOL_INSTRUCTIONS_FILE
from src.dialogues.abstracts.abstract_factories import InitialPromptingMessagesFactory
from src.dialogues.abstracts.factory_products import InitialPromptingMessagesProduct
from src.dialogues.factories.character_choice_dialogue_system_content_for_prompt_factory import \
    CharacterChoiceDialogueSystemContentForPromptFactory
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.products.concrete_initial_prompting_messages_product import ConcreteInitialPromptingMessagesProduct


class CharacterChoiceDialogueInitialPromptingMessagesFactory(InitialPromptingMessagesFactory):
    def __init__(self, participants: List[dict], player_identifier: Optional[int], dialogue: List[dict[Any, str]]):
        assert participants
        assert not isinstance(dialogue, NoneType)

        self._participants = participants
        self._player_identifier = player_identifier
        self._dialogue = dialogue

    def create_initial_prompting_messages(self) -> InitialPromptingMessagesProduct:
        filesystem_manager = FilesystemManager()

        return ConcreteInitialPromptingMessagesProduct([{"role": "system",
                                                         "content": CharacterChoiceDialogueSystemContentForPromptFactory(
                                                             self._participants, self._player_identifier,
                                                             self._dialogue,
                                                             filesystem_manager.read_file(
                                                                 CHOOSING_SPEECH_TURN_PROMPT_FILE),
                                                             filesystem_manager.read_json_file(SPEECH_TURN_TOOL_FILE),
                                                             filesystem_manager.read_file(
                                                                 TOOL_INSTRUCTIONS_FILE)).create_system_content_for_prompt().get()},
                                                        {"role": "user",
                                                         "content": f"Here's an example: Choose who will speak next in this dialogue."},
                                                        {"role": "assistant",
                                                         "content": f"<function=choose_speech_turn>{{\"identifier\": \"1\", \"name\": \"Bob\"}}</function>"},
                                                        {"role": "user",
                                                         "content": f"Here's another example: Choose who will speak next in this dialogue."},
                                                        {"role": "assistant",
                                                         "content": f"<function=choose_speech_turn>{{\"identifier\": \"2\", \"name\": \"Alice\"}}</function>"},
                                                        {"role": "user",
                                                         "content": "Choose who will speak next in this dialogue."}])
