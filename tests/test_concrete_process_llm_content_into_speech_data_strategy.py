from unittest.mock import MagicMock

import pytest

from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.products.concrete_speech_data_product import (
    ConcreteSpeechDataProduct,
)
from src.dialogues.strategies.concrete_process_llm_content_into_speech_data_strategy import (
    ConcreteProcessLlmContentIntoSpeechDataStrategy,
)
from src.prompting.abstracts.factory_products import LlmContentProduct
from src.prompting.factories.speech_tool_response_data_extraction_provider_factory import (
    SpeechToolResponseDataExtractionProviderFactory,
)
from src.prompting.factories.tool_response_parsing_provider_factory import (
    ToolResponseParsingProviderFactory,
)


@pytest.fixture
def mock_dependencies():
    messages_to_llm = MagicMock(spec=MessagesToLlm)
    tool_response_parsing_provider_factory = MagicMock(
        spec=ToolResponseParsingProviderFactory
    )
    speech_tool_response_data_extraction_provider_factory = MagicMock(
        spec=SpeechToolResponseDataExtractionProviderFactory
    )
    return {
        "messages_to_llm": messages_to_llm,
        "tool_response_parsing_provider_factory": tool_response_parsing_provider_factory,
        "speech_tool_response_data_extraction_provider_factory": speech_tool_response_data_extraction_provider_factory,
    }


@pytest.fixture
def strategy(mock_dependencies):
    return ConcreteProcessLlmContentIntoSpeechDataStrategy(
        messages_to_llm=mock_dependencies["messages_to_llm"],
        tool_response_parsing_provider_factory=mock_dependencies[
            "tool_response_parsing_provider_factory"
        ],
        speech_tool_response_data_extraction_provider_factory=mock_dependencies[
            "speech_tool_response_data_extraction_provider_factory"
        ],
    )


def test_do_algorithm_with_invalid_llm_content(strategy):
    llm_content_product = MagicMock(spec=LlmContentProduct)
    llm_content_product.is_valid.return_value = False
    llm_content_product.get_error.return_value = "Invalid LLM content"
    result = strategy.do_algorithm(llm_content_product)
    assert isinstance(result, ConcreteSpeechDataProduct)
    assert not result.is_valid()
    assert result.get_error() == "Invalid LLM content"


def test_do_algorithm_with_invalid_parsed_tool_response(strategy, mock_dependencies):
    llm_content_product = MagicMock(spec=LlmContentProduct)
    llm_content_product.is_valid.return_value = True
    llm_content_product.get.return_value = "Some valid LLM content"
    tool_response_parsing_product = MagicMock()
    tool_response_parsing_product.is_valid.return_value = False
    tool_response_parsing_product.get.return_value = "Some invalid parsed content"
    tool_response_parsing_product.get_error.return_value = "Parsing error"
    (
        mock_dependencies[
            "tool_response_parsing_provider_factory"
        ].create_tool_response_parsing_provider.return_value.parse_tool_response.return_value
    ) = tool_response_parsing_product
    result = strategy.do_algorithm(llm_content_product)
    assert isinstance(result, ConcreteSpeechDataProduct)
    assert not result.is_valid()
    assert "Was unable to parse the tool response" in result.get_error()
