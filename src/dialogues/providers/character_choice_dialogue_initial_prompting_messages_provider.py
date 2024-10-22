from src.dialogues.abstracts.abstract_factories import InitialPromptingMessagesProvider
from src.dialogues.abstracts.factory_products import InitialPromptingMessagesProduct
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.providers.character_choice_dialogue_system_content_for_prompt_provider import \
    CharacterChoiceDialogueSystemContentForPromptProvider
from src.prompting.products.concrete_initial_prompting_messages_product import ConcreteInitialPromptingMessagesProduct


class CharacterChoiceDialogueInitialPromptingMessagesProvider(
    InitialPromptingMessagesProvider):

    def __init__(self,
                 character_choice_dialogue_system_content_for_prompt_factory:
                 CharacterChoiceDialogueSystemContentForPromptProvider):
        (self._character_choice_dialogue_system_content_for_prompt_factory
         ) = character_choice_dialogue_system_content_for_prompt_factory

    def create_initial_prompting_messages(self
                                          ) -> InitialPromptingMessagesProduct:
        messages_to_llm = MessagesToLlm()
        messages_to_llm.add_message('system', self.
                                    _character_choice_dialogue_system_content_for_prompt_factory.
                                    create_system_content_for_prompt().get())
        messages_to_llm.add_message('user',
                                    f"Here's an example: Choose who will speak next in this dialogue.")
        messages_to_llm.add_message('assistant',
                                    f'<function=choose_speech_turn>{{"identifier": "1", "name": "Bob"}}</function>'
                                    )
        messages_to_llm.add_message('user',
                                    f"Here's another example: Choose who will speak next in this dialogue."
                                    )
        messages_to_llm.add_message('assistant',
                                    f'<function=choose_speech_turn>{{"identifier": "2", "name": "Alice"}}</function>'
                                    )
        messages_to_llm.add_message('user',
                                    'Choose who will speak next in this dialogue. Choose only among the allowed participants.'
                                    )
        return ConcreteInitialPromptingMessagesProduct(messages_to_llm)
