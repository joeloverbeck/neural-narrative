from typing import List

from src.constants import TOOL_INSTRUCTIONS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import SystemContentForPromptFactory
from src.prompting.abstracts.factory_products import SystemContentForPromptProduct
from src.prompting.products.concrete_system_content_for_prompt_product import ConcreteSystemContentForPromptProduct
from src.tools import generate_tool_prompt


class SpeechTurnDialogueSystemContentForPromptFactory(SystemContentForPromptFactory):
    def __init__(self, playthrough_name: str, participants: List[dict], character_data: dict, memories: str,
                 prompt_file: str,
                 tool_file: str):
        assert playthrough_name
        assert len(participants) >= 2
        assert character_data
        assert prompt_file
        assert tool_file

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._character_data = character_data
        self._memories = memories
        self._prompt_file = prompt_file
        self._tool_file = tool_file

    def create_system_content_for_prompt(self) -> SystemContentForPromptProduct:
        filesystem_manager = FilesystemManager()
        prompt_template = filesystem_manager.read_file(self._prompt_file)
        tool_data = filesystem_manager.read_json_file(self._tool_file)

        # It's necessary to format some of the values in tool_data with actual values.
        replacements = {
            "name": self._character_data["name"]
        }

        tool_data['function']['description'] = tool_data['function']['description'].format(**replacements)
        tool_data['function']['parameters']['properties']['narration_text']['description'] = \
            tool_data['function']['parameters']['properties']['narration_text']['description'].format(
                **replacements)
        tool_data['function']['parameters']['properties']['name']['description'] = \
            tool_data['function']['parameters']['properties']['name']['description'].format(**replacements)
        tool_data['function']['parameters']['properties']['speech']['description'] = \
            tool_data['function']['parameters']['properties']['speech']['description'].format(**replacements)

        participant_details = "\n".join(
            [f'{participant["name"]}: {participant["description"]}' for participant in self._participants if
             participant["name"] != self._character_data["name"]])

        # Retrieve the details of the world
        playthrough_metadata_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        worlds_template = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_worlds_template_file())

        return ConcreteSystemContentForPromptProduct(prompt_template.format(
            world_name=playthrough_metadata_file["world_template"],
            world_description=worlds_template[playthrough_metadata_file["world_template"]]["description"],
            name=self._character_data["name"],
            participant_details=participant_details,
            description=self._character_data["description"],
            personality=self._character_data["personality"],
            profile=self._character_data["profile"],
            likes=self._character_data["likes"],
            dislikes=self._character_data["dislikes"],
            first_message=self._character_data["first message"],
            speech_patterns=self._character_data["speech patterns"],
            memories=self._memories
        ) + "\n\n" + generate_tool_prompt(tool_data, filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE)),
                                                     is_valid=True)
