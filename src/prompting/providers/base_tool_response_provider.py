import logging
from abc import abstractmethod
from pathlib import Path
from typing import Optional, Type

from pydantic import BaseModel

from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.algorithms.tokenize_algorithm import TokenizeAlgorithm

logger = logging.getLogger(__name__)


class BaseToolResponseProvider:
    """
    Base class providing common functionality for generating tool responses.
    """

    def __init__(
        self,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

        self._path_manager = path_manager or PathManager()

    @staticmethod
    def _read_prompt_file(prompt_file: Path) -> str:
        """Reads a prompt file from the filesystem."""
        return read_file(prompt_file)

    def _read_tool_instructions(self) -> str:
        """Reads the tool instructions from the filesystem."""
        return read_file(self._path_manager.get_tool_instructions_for_instructor_path())

    @staticmethod
    def _format_prompt(prompt_template: str, **kwargs) -> str:
        """Formats a prompt template with provided keyword arguments."""
        return prompt_template.format(**kwargs)

    @staticmethod
    def _generate_system_content(prompt: str, tool_prompt: str) -> str:
        """Generates the system content by combining the prompt and tool prompt."""
        system_content = f"{prompt}\n{tool_prompt}"
        logger.info(
            "System content token amount: %s tokens.",
            TokenizeAlgorithm(system_content).do_algorithm(),
        )
        return system_content

    def _produce_tool_response(
        self, system_content: str, user_content: str, response_model: Type[BaseModel]
    ):
        """Produces the tool response using the strategy factory."""
        strategy = (
            self._produce_tool_response_strategy_factory.create_produce_tool_response_strategy()
        )

        tool_response = strategy.produce_tool_response(
            system_content, user_content, response_model
        )

        if isinstance(tool_response, BaseModel):
            return self.create_product_from_base_model(tool_response)
        else:
            raise NotImplementedError(
                f"Case not implemented for when the tool response is of type '{type(tool_response)}.'"
            )

    def peep_into_system_content(self, system_content: str):
        pass

    @staticmethod
    def _generate_tool_prompt(tool_data: dict, tool_instructions: str) -> str:
        return f"{tool_instructions} {tool_data}"

    def generate_product(self, response_model: Type[BaseModel]):
        formatted_prompt = self.get_formatted_prompt()
        if formatted_prompt is None:
            prompt_file = self.get_prompt_file()
            prompt_kwargs = self.get_prompt_kwargs()
            prompt_template = self._read_prompt_file(prompt_file)
            formatted_prompt = self._format_prompt(prompt_template, **prompt_kwargs)
        tool_data = self._get_tool_data(response_model)
        tool_instructions = self._read_tool_instructions()
        tool_prompt = self._generate_tool_prompt(tool_data, tool_instructions)
        system_content = self._generate_system_content(formatted_prompt, tool_prompt)
        logger.info(system_content)
        self.peep_into_system_content(system_content)
        user_content = self.get_user_content()
        return self._produce_tool_response(system_content, user_content, response_model)

    @staticmethod
    def _get_tool_data(response_model: Type[BaseModel]) -> dict:
        return response_model.model_json_schema()

    @abstractmethod
    def get_user_content(self) -> str:
        raise NotImplemented("Should be implemented.")

    def create_product_from_base_model(self, response_model: BaseModel):
        raise NotImplemented(
            "Detected that the tool response was a BaseModel, so this should be implemented."
        )

    def get_prompt_file(self) -> Optional[Path]:
        raise NotImplemented("Should be implemented.")

    def get_prompt_kwargs(self) -> dict:
        raise NotImplemented("Should be implemented.")

    def get_formatted_prompt(self) -> Optional[str]:
        return None
