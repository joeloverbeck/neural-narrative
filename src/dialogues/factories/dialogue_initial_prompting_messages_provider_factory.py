from src.characters.character import Character
from src.dialogues.factories.speech_turn_dialogue_system_content_for_prompt_provider_factory import (
    SpeechTurnDialogueSystemContentForPromptProviderFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.providers.dialogue_initial_prompting_messages_provider import (
    DialogueInitialPromptingMessagesProvider,
)
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class DialogueInitialPromptingMessagesProviderFactory:

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        speech_turn_dialogue_system_content_for_prompt_provider_factory: SpeechTurnDialogueSystemContentForPromptProviderFactory,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")
        self._playthrough_name = playthrough_name
        self._participants = participants
        (self._speech_turn_dialogue_system_content_for_prompt_provider_factory) = (
            speech_turn_dialogue_system_content_for_prompt_provider_factory
        )

    def create_dialogue_initial_prompting_messages_provider(
        self, speech_turn_tool_response_product: LlmToolResponseProduct
    ) -> DialogueInitialPromptingMessagesProvider:
        if not isinstance(speech_turn_tool_response_product.get()["identifier"], str):
            raise TypeError(
                f"Received an identifier that wasn't a string, but a {type(speech_turn_tool_response_product.get()['identifier'])}: {speech_turn_tool_response_product.get()['identifier']}"
            )
        character = Character(
            self._playthrough_name,
            speech_turn_tool_response_product.get()["identifier"],
        )
        return DialogueInitialPromptingMessagesProvider(
            self._participants,
            character,
            self._speech_turn_dialogue_system_content_for_prompt_provider_factory,
        )
