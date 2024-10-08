from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from src.prompting.abstracts.factory_products import (
    LlmToolResponseProduct,
    ExtractedDataProduct,
    LlmContentProduct,
    ToolResponseParsingProduct,
    SystemContentForPromptProduct,
    UserContentForCharacterGenerationProduct,
    FilteredPlaceDescriptionGenerationProduct,
)
from src.prompting.abstracts.llm_client import LlmClient


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
    def generate_content(self) -> LlmContentProduct:
        pass


class SystemContentForPromptProvider(ABC):
    @abstractmethod
    def create_system_content_for_prompt(self) -> SystemContentForPromptProduct:
        pass


class LlmClientFactory(ABC):
    @abstractmethod
    def create_llm_client(self) -> LlmClient:
        pass


class UserContentForCharacterGenerationFactory(Protocol):
    def create_user_content_for_character_generation(
        self,
    ) -> UserContentForCharacterGenerationProduct:
        pass


class FilteredPlaceDescriptionGenerationFactory(Protocol):
    def generate_filtered_place_description(
        self,
    ) -> FilteredPlaceDescriptionGenerationProduct:
        pass
