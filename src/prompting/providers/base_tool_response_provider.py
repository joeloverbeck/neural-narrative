from abc import abstractmethod
from typing import Optional

from src.base.constants import TOOL_INSTRUCTIONS_FILE
from src.base.required_string import RequiredString
from src.base.tools import generate_tool_prompt
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class BaseToolResponseProvider:
    """
    Base class providing common functionality for generating tool responses.
    """

    def __init__(
        self,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: FilesystemManager = None,
    ):
        if not produce_tool_response_strategy_factory:
            raise ValueError("produce_tool_response_strategy_factory must not be None.")

        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _read_prompt_file(self, prompt_file: RequiredString) -> RequiredString:
        """Reads a prompt file from the filesystem."""
        return self._filesystem_manager.read_file(prompt_file)

    def _read_tool_file(self, tool_file: RequiredString) -> dict:
        """Reads a tool file (JSON) from the filesystem."""
        return self._filesystem_manager.read_json_file(tool_file)

    def _read_tool_instructions(self) -> RequiredString:
        """Reads the tool instructions from the filesystem."""
        return self._filesystem_manager.read_file(
            RequiredString(TOOL_INSTRUCTIONS_FILE)
        )

    @staticmethod
    def _generate_tool_prompt(
            tool_data: dict, tool_instructions: RequiredString
    ) -> RequiredString:
        """Generates the tool prompt by combining tool data and instructions."""
        return generate_tool_prompt(tool_data, tool_instructions)

    @staticmethod
    def _format_prompt(prompt_template: RequiredString, **kwargs) -> RequiredString:
        """Formats a prompt template with provided keyword arguments."""
        return RequiredString(prompt_template.value.format(**kwargs))

    @staticmethod
    def _generate_system_content(
            prompt: RequiredString, tool_prompt: RequiredString
    ) -> RequiredString:
        """Generates the system content by combining the prompt and tool prompt."""
        return RequiredString(f"{prompt}\n\n{tool_prompt}")

    def _produce_tool_response(
            self, system_content: RequiredString, user_content: RequiredString
    ) -> dict:
        if not isinstance(system_content, RequiredString):
            system_content = RequiredString(system_content)
        if not isinstance(user_content, RequiredString):
            user_content = RequiredString(user_content)

        """Produces the tool response using the strategy factory."""
        strategy = (
            self._produce_tool_response_strategy_factory.create_produce_tool_response_strategy()
        )

        return strategy.produce_tool_response(system_content, user_content)

    @staticmethod
    def _extract_arguments(tool_response: dict) -> dict:
        """Extracts arguments from the tool response."""
        return tool_response.get("arguments", {})

    def peep_into_system_content(self, system_content: RequiredString):
        pass

    def peep_into_tool_response(self, tool_response: dict):
        pass

    def generate_product(self):
        # Prepare the prompt
        formatted_prompt = self.get_formatted_prompt()
        if formatted_prompt is None:
            prompt_file = self.get_prompt_file()
            prompt_kwargs = self.get_prompt_kwargs()
            prompt_template = self._read_prompt_file(prompt_file)
            formatted_prompt = self._format_prompt(prompt_template, **prompt_kwargs)

        # Generate system content
        tool_file = self.get_tool_file()
        tool_data = self._read_tool_file(tool_file)
        tool_instructions = self._read_tool_instructions()
        tool_prompt = self._generate_tool_prompt(tool_data, tool_instructions)
        system_content = RequiredString(
            self._generate_system_content(formatted_prompt, tool_prompt)
        )

        self.peep_into_system_content(system_content)

        # User content
        user_content = RequiredString(self.get_user_content())

        # Produce tool response
        tool_response = self._produce_tool_response(system_content, user_content)

        self.peep_into_tool_response(tool_response)

        # Extract arguments
        arguments = self._extract_arguments(tool_response)

        # Create and return the product
        product = self.create_product(arguments)

        return product

    @abstractmethod
    def get_tool_file(self) -> RequiredString:
        pass

    @abstractmethod
    def get_user_content(self) -> RequiredString:
        pass

    @abstractmethod
    def create_product(self, arguments: dict):
        pass

    def get_prompt_file(self) -> Optional[RequiredString]:
        return None

    def get_prompt_kwargs(self) -> dict:
        return {}

    def get_formatted_prompt(self) -> Optional[RequiredString]:
        return None
