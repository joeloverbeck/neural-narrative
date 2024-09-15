from src.dialogues.factories.character_choice_dialogue_system_content_for_prompt_provider_factory import \
    CharacterChoiceDialogueSystemContentForPromptProviderFactory
from src.dialogues.participants import Participants
from src.dialogues.providers.character_choice_dialogue_initial_prompting_messages_provider import \
    CharacterChoiceDialogueInitialPromptingMessagesProvider
from src.dialogues.transcription import Transcription


class CharacterChoiceDialogueInitialPromptingMessagesProviderFactory:
    def __init__(self,
                 character_choice_dialogue_system_content_for_prompt_provider_factory: CharacterChoiceDialogueSystemContentForPromptProviderFactory):
        self._character_choice_dialogue_system_content_for_prompt_provider_factory = character_choice_dialogue_system_content_for_prompt_provider_factory

    def create_character_choice_dialogue_initial_prompting_messages_provider(
            self, participants: Participants,
            transcription: Transcription) -> CharacterChoiceDialogueInitialPromptingMessagesProvider:
        return CharacterChoiceDialogueInitialPromptingMessagesProvider(
            self._character_choice_dialogue_system_content_for_prompt_provider_factory.create_character_choice_dialogue_system_content_for_prompt_provider(
                participants, transcription))
