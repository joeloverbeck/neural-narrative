from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from src.prompting.abstracts.factory_products import LlmToolResponseProduct, ExtractedDataProduct, LlmContentProduct, \
    ToolResponseParsingProduct, SystemContentForPromptProduct, AiCompletionProduct


class ToolResponseParsingFactory(ABC):
    @abstractmethod
    def parse_tool_response(self) -> ToolResponseParsingProduct:
        pass


class ToolResponseFactory(ABC):
    """
    The Abstract Factory interface declares a set of methods that return
    different abstract products. These products are called a family and are
    related by a high-level theme or concept. Products of one family are usually
    able to collaborate among themselves. A family of products may have several
    variants, but the products of one variant are incompatible with products of
    another.
    """

    @abstractmethod
    def create_llm_response(self) -> LlmToolResponseProduct:
        pass


class ToolResponseDataExtractionFactory(ABC):
    @abstractmethod
    def extract_data(self) -> ExtractedDataProduct:
        pass


class AiCompletionFactory(ABC):
    @abstractmethod
    def generate_completion(self, model: str, messages: List[dict], temperature=1.0, top_p=1.0) -> AiCompletionProduct:
        pass


class LlmContentFactory(ABC):
    @abstractmethod
    def generate_content(self) -> LlmContentProduct:
        pass


class SystemContentForPromptFactory(ABC):
    @abstractmethod
    def create_system_content_for_prompt(self) -> SystemContentForPromptProduct:
        pass
