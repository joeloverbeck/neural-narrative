from src.characters.character import Character
from src.dialogues.abstracts.abstract_factories import InitialPromptingMessagesProvider
from src.dialogues.abstracts.factory_products import InitialPromptingMessagesProduct
from src.dialogues.factories.speech_turn_dialogue_system_content_for_prompt_provider_factory import (
    SpeechTurnDialogueSystemContentForPromptProviderFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.prompting.products.concrete_initial_prompting_messages_product import (
    ConcreteInitialPromptingMessagesProduct,
)


class DialogueInitialPromptingMessagesProvider(InitialPromptingMessagesProvider):
    def __init__(
        self,
        participants: Participants,
        character: Character,
        memories: str,
        speech_turn_dialogue_system_content_for_prompt_provider_factory: SpeechTurnDialogueSystemContentForPromptProviderFactory,
    ):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._participants = participants
        self._character = character
        self._memories = memories
        self._speech_turn_dialogue_system_content_for_prompt_provider_factory = (
            speech_turn_dialogue_system_content_for_prompt_provider_factory
        )

    def create_initial_prompting_messages(self) -> InitialPromptingMessagesProduct:
        other_character_name: str = "[CHARACTER]"

        for identifier, character in self._participants.get().items():
            if character["name"] != self._character.name:
                other_character_name = character["name"]
                break

        system_content_for_prompt_product = self._speech_turn_dialogue_system_content_for_prompt_provider_factory.create_speech_turn_dialogue_system_content_for_prompt_provider(
            self._participants, self._character, self._memories
        ).create_system_content_for_prompt()

        if not system_content_for_prompt_product.is_valid():
            raise ValueError(
                f"Failed to produce the system content for the speech turn: {system_content_for_prompt_product.get_error()}"
            )

        messages_to_llm = MessagesToLlm()

        messages_to_llm.add_message("system", system_content_for_prompt_product.get())

        messages_to_llm.add_message(
            "user",
            f"Here's an example: {other_character_name}: What's up?",
            is_guiding_message=True,
        )
        messages_to_llm.add_message(
            "assistant",
            f'<function=generate_speech>{{"name": "{self._character.name}", "speech": "What\'s up with you?", "narration_text": "{self._character.name} stares at {other_character_name}." }}</function>',
            is_guiding_message=True,
        )
        messages_to_llm.add_message(
            "user",
            f"Here's a second example: {other_character_name}: Hello.",
            is_guiding_message=True,
        )
        messages_to_llm.add_message(
            "assistant",
            f'<function=generate_speech>{{"name": "{self._character.name}", "speech": "Hey.", "narration_text": "{self._character.name} stares at {other_character_name}." }}</function>',
            is_guiding_message=True,
        )

        return ConcreteInitialPromptingMessagesProduct(messages_to_llm)
