from src.constants import (
    INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE,
    INTERESTING_SITUATIONS_GENERATION_TOOL_FILE,
)
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.events.products.interesting_situations_product import (
    InterestingSituationsProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class InterestingSituationsFactory(BaseToolResponseProvider):
    def __init__(
        self,
        transcription: Transcription,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: FilesystemManager = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._transcription = transcription

    def generate_interesting_situations(self) -> InterestingSituationsProduct:
        # Prepare the prompt
        prompt_template = self._read_prompt_file(
            INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE
        )
        formatted_prompt = self._format_prompt(
            prompt_template, transcription=self._transcription.get()
        )

        # Generate system content
        tool_data = self._read_tool_file(INTERESTING_SITUATIONS_GENERATION_TOOL_FILE)
        tool_instructions = self._read_tool_instructions()
        tool_prompt = self._generate_tool_prompt(tool_data, tool_instructions)
        system_content = self._generate_system_content(formatted_prompt, tool_prompt)

        # User content
        user_content = "Write a list of at least five very interesting and intriguing situations that could stem from this conversation, as per the above instructions."

        # Produce tool response
        tool_response = self._produce_tool_response(system_content, user_content)

        # Extract arguments
        arguments = self._extract_arguments(tool_response)

        return InterestingSituationsProduct(
            arguments.get("interesting_situations"), is_valid=True
        )
