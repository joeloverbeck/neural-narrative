from src.characters.character import Character
from src.constants import TOOL_INSTRUCTIONS_FILE
from src.dialogues.abstracts.strategies import PromptFormatterForDialogueStrategy
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import SystemContentForPromptProvider
from src.prompting.abstracts.factory_products import SystemContentForPromptProduct
from src.prompting.products.concrete_system_content_for_prompt_product import (
    ConcreteSystemContentForPromptProduct,
)
from src.tools import generate_tool_prompt


class SpeechTurnDialogueSystemContentForPromptProvider(SystemContentForPromptProvider):
    def __init__(
        self,
        character: Character,
        tool_file: str,
        prompt_formatter_for_dialogue_strategy: PromptFormatterForDialogueStrategy,
    ):
        assert tool_file
        assert prompt_formatter_for_dialogue_strategy

        self._character = character
        self._tool_file = tool_file
        self._prompt_formatter_for_dialogue_strategy = (
            prompt_formatter_for_dialogue_strategy
        )

    def create_system_content_for_prompt(self) -> SystemContentForPromptProduct:
        filesystem_manager = FilesystemManager()
        tool_data = filesystem_manager.read_json_file(self._tool_file)

        # It's necessary to format some of the values in tool_data with actual values.
        replacements = {"name": self._character.name}

        tool_data["function"]["description"] = tool_data["function"][
            "description"
        ].format(**replacements)
        tool_data["function"]["parameters"]["properties"]["narration_text"][
            "description"
        ] = tool_data["function"]["parameters"]["properties"]["narration_text"][
            "description"
        ].format(
            **replacements
        )
        tool_data["function"]["parameters"]["properties"]["name"]["description"] = (
            tool_data["function"]["parameters"]["properties"]["name"][
                "description"
            ].format(**replacements)
        )
        tool_data["function"]["parameters"]["properties"]["speech"]["description"] = (
            tool_data["function"]["parameters"]["properties"]["speech"][
                "description"
            ].format(**replacements)
        )

        return ConcreteSystemContentForPromptProduct(
            self._prompt_formatter_for_dialogue_strategy.do_algorithm()
            + "\n\n"
            + generate_tool_prompt(
                tool_data, filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE)
            ),
            is_valid=True,
        )
