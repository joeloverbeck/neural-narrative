from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from src.base.constants import MAX_RETRIES
from src.dialogues.messages_to_llm import MessagesToLlm
from src.base.enums import AiCompletionErrorType
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.providers.concrete_llm_content_provider import ConcreteLlmContentProvider


# Fixture to mock LlmClient and its responses
@pytest.fixture
def llm_client_mock():
    return MagicMock(spec=LlmClient)


@pytest.fixture
def messages_to_llm():
    return MessagesToLlm()  # or provide a mock if you don't have a concrete implementation


@pytest.fixture
def concrete_factory(llm_client_mock, messages_to_llm):
    return ConcreteLlmContentProvider(
        model="test-model",
        messages_to_llm=messages_to_llm,
        llm_client=cast(LlmClient, llm_client_mock)
    )


def test_generate_content_success(concrete_factory, llm_client_mock):
    # Mocking a valid completion response
    completion_product = MagicMock()
    completion_product.is_valid.return_value = True
    completion_product.get.return_value = "Test content"

    llm_client_mock.generate_completion.return_value = completion_product

    # Test generate_content behavior
    result = concrete_factory.generate_content()

    assert result.is_valid()
    assert result.get() == "Test content"
    llm_client_mock.generate_completion.assert_called_once()


@patch("src.prompting.providers.concrete_llm_content_provider.sleep")
def test_generate_content_too_many_requests_retry(sleep_mock, concrete_factory, llm_client_mock):
    # Mocking a TOO_MANY_REQUESTS error on the first attempt and valid on the second
    completion_product_error = MagicMock()
    completion_product_error.is_valid.return_value = False
    completion_product_error.get_error.return_value = AiCompletionErrorType.TOO_MANY_REQUESTS

    completion_product_valid = MagicMock()
    completion_product_valid.is_valid.return_value = True
    completion_product_valid.get.return_value = "Valid content after retry"

    llm_client_mock.generate_completion.side_effect = [completion_product_error, completion_product_valid]

    # Test that the content is eventually generated after a retry
    result = concrete_factory.generate_content()

    assert result.is_valid()
    assert result.get() == "Valid content after retry"
    assert llm_client_mock.generate_completion.call_count == 2
    sleep_mock.assert_called_once()  # Ensure sleep is called for retry


@patch("src.prompting.providers.concrete_llm_content_provider.sleep")
def test_generate_content_max_retries_exceeded(sleep_mock, concrete_factory, llm_client_mock):
    # Mocking a TOO_MANY_REQUESTS error for every retry
    completion_product_error = MagicMock()
    completion_product_error.is_valid.return_value = False
    completion_product_error.get_error.return_value = AiCompletionErrorType.TOO_MANY_REQUESTS

    llm_client_mock.generate_completion.return_value = completion_product_error

    # Test that after MAX_RETRIES, it returns an invalid result
    result = concrete_factory.generate_content()

    assert result.get() == ""
    assert result.get_error() == "Max retries reached. No valid response."
    assert not result.is_valid()
    assert llm_client_mock.generate_completion.call_count == MAX_RETRIES
    assert sleep_mock.call_count == MAX_RETRIES - 1  # sleep is called for each retry except the last


@patch("src.prompting.providers.concrete_llm_content_provider.sleep")
def test_generate_content_unauthorized_retry(sleep_mock, concrete_factory, llm_client_mock):
    # Mocking an UNAUTHORIZED error on the first attempt and valid on the second
    completion_product_error = MagicMock()
    completion_product_error.is_valid.return_value = False
    completion_product_error.get_error.return_value = AiCompletionErrorType.UNAUTHORIZED

    completion_product_valid = MagicMock()
    completion_product_valid.is_valid.return_value = True
    completion_product_valid.get.return_value = "Valid content after retry"

    llm_client_mock.generate_completion.side_effect = [completion_product_error, completion_product_valid]

    # Test that the content is eventually generated after a retry
    result = concrete_factory.generate_content()

    assert result.is_valid()
    assert result.get() == "Valid content after retry"
    assert llm_client_mock.generate_completion.call_count == 2
    sleep_mock.assert_called_once()
