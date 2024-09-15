from src.constants import CHOOSING_SPEECH_TURN_PROMPT_FILE, SPEECH_TURN_TOOL_FILE, TOOL_INSTRUCTIONS_FILE
from src.dialogues.participants import Participants
from src.dialogues.providers.character_choice_dialogue_system_content_for_prompt_provider import \
    CharacterChoiceDialogueSystemContentForPromptProvider
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager


class CharacterChoiceDialogueSystemContentForPromptProviderFactory:
    def __init__(self, player_identifier: str, filesystem_manager: FilesystemManager = None):
        if not player_identifier:
            raise ValueError("player_identifier must not be empty.")

        self._player_identifier = player_identifier

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def create_character_choice_dialogue_system_content_for_prompt_provider(
            self, participants: Participants,
            transcription: Transcription) -> CharacterChoiceDialogueSystemContentForPromptProvider:
        return CharacterChoiceDialogueSystemContentForPromptProvider(
            participants, self._player_identifier,
            transcription,
            self._filesystem_manager.read_file(
                CHOOSING_SPEECH_TURN_PROMPT_FILE),
            self._filesystem_manager.read_json_file(
                SPEECH_TURN_TOOL_FILE),
            self._filesystem_manager.read_file(
                TOOL_INSTRUCTIONS_FILE))
