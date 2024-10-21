from src.base.constants import (
    CHOOSING_SPEECH_TURN_PROMPT_FILE,
    SPEECH_TURN_TOOL_FILE,
    TOOL_INSTRUCTIONS_FILE,
)
from src.base.required_string import RequiredString
from src.dialogues.participants import Participants
from src.dialogues.providers.character_choice_dialogue_system_content_for_prompt_provider import (
    CharacterChoiceDialogueSystemContentForPromptProvider,
)
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager


class CharacterChoiceDialogueSystemContentForPromptProviderFactory:
    def __init__(
            self,
            player_identifier: RequiredString,
            filesystem_manager: FilesystemManager = None,
    ):
        self._player_identifier = player_identifier

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def create_character_choice_dialogue_system_content_for_prompt_provider(
            self, participants: Participants, transcription: Transcription
    ) -> CharacterChoiceDialogueSystemContentForPromptProvider:
        return CharacterChoiceDialogueSystemContentForPromptProvider(
            participants,
            self._player_identifier,
            transcription,
            self._filesystem_manager.read_file(
                RequiredString(CHOOSING_SPEECH_TURN_PROMPT_FILE)
            ),
            self._filesystem_manager.read_json_file(
                RequiredString(SPEECH_TURN_TOOL_FILE)
            ),
            self._filesystem_manager.read_file(RequiredString(TOOL_INSTRUCTIONS_FILE)),
        )
