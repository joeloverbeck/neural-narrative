from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, Type

from pydantic import BaseModel

from src.prompting.abstracts.factory_products import (
    LlmToolResponseProduct,
    ExtractedDataProduct,
    LlmContentProduct,
    ToolResponseParsingProduct,
    UserContentForCharacterGenerationProduct,
)
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy


class ToolResponseParsingProvider(ABC):

    @abstractmethod
    def parse_tool_response(self) -> ToolResponseParsingProduct:
        pass


class ToolResponseProvider(Protocol):

    def create_llm_response(self) -> LlmToolResponseProduct:
        pass


class ToolResponseDataExtractionProvider(ABC):

    @abstractmethod
    def extract_data(self) -> ExtractedDataProduct:
        pass


class LlmContentProvider(ABC):

    @abstractmethod
    def generate_content(self, response_model: Type[BaseModel]) -> LlmContentProduct:
        pass


class LlmClientFactory(ABC):

    @abstractmethod
    def create_llm_client(self, response_model: Type[BaseModel]) -> LlmClient:
        pass


class UserContentForCharacterGenerationFactory(Protocol):

    def create_user_content_for_character_generation(
        self,
    ) -> UserContentForCharacterGenerationProduct:
        pass


class ProduceToolResponseStrategyFactory(Protocol):
    def create_produce_tool_response_strategy(self) -> ProduceToolResponseStrategy:
        pass
