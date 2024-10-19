from unittest.mock import MagicMock

import pytest

from src.base.constants import MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL
from src.dialogues.providers.llm_speech_data_provider import LlmSpeechDataProvider


@pytest.fixture
def setup_llm_speech_data_provider():
    # Mock dependencies
    messages_to_llm = MagicMock()
    llm_content_provider_factory = MagicMock()
    process_llm_content_strategy = MagicMock()

    # Create the class instance with the mocks
    provider = LlmSpeechDataProvider(messages_to_llm, llm_content_provider_factory, process_llm_content_strategy)

    return provider, messages_to_llm, llm_content_provider_factory, process_llm_content_strategy


def test_create_speech_data_valid_first_attempt(setup_llm_speech_data_provider):
    provider, _, llm_content_provider_factory, process_llm_content_strategy = setup_llm_speech_data_provider

    # Mock behavior for valid speech data on the first attempt
    llm_content_product = MagicMock()
    valid_speech_data_product = MagicMock()
    valid_speech_data_product.is_valid.return_value = True

    # Mock the content provider's generate_content method
    llm_content_provider = MagicMock()
    llm_content_provider.generate_content.return_value = llm_content_product
    llm_content_provider_factory.create_llm_content_provider.return_value = llm_content_provider

    # Mock the strategy's do_algorithm method to return valid speech data
    process_llm_content_strategy.do_algorithm.return_value = valid_speech_data_product

    # Call the method under test
    speech_data = provider.create_speech_data()

    # Verify that the valid speech data was returned
    assert speech_data.is_valid()

    # Verify that the strategy and content provider were called exactly once
    llm_content_provider.generate_content.assert_called_once()
    process_llm_content_strategy.do_algorithm.assert_called_once_with(llm_content_product)


def test_create_speech_data_with_retries(setup_llm_speech_data_provider):
    provider, _, llm_content_provider_factory, process_llm_content_strategy = setup_llm_speech_data_provider

    # Mock behavior for invalid speech data on the first attempt, valid on the second
    llm_content_product = MagicMock()
    invalid_speech_data_product = MagicMock()
    invalid_speech_data_product.is_valid.return_value = False

    valid_speech_data_product = MagicMock()
    valid_speech_data_product.is_valid.return_value = True

    # Mock the content provider's generate_content method
    llm_content_provider = MagicMock()
    llm_content_provider.generate_content.return_value = llm_content_product
    llm_content_provider_factory.create_llm_content_provider.return_value = llm_content_provider

    # Mock the strategy's do_algorithm method to return invalid first, valid second
    process_llm_content_strategy.do_algorithm.side_effect = [
        invalid_speech_data_product,
        valid_speech_data_product
    ]

    # Call the method under test
    speech_data = provider.create_speech_data()

    # Verify that the valid speech data was returned on the second attempt
    assert speech_data.is_valid()

    # Verify that the strategy and content provider were called twice
    assert llm_content_provider.generate_content.call_count == 2
    assert process_llm_content_strategy.do_algorithm.call_count == 2


def test_create_speech_data_max_retries_exhausted(setup_llm_speech_data_provider):
    provider, _, llm_content_provider_factory, process_llm_content_strategy = setup_llm_speech_data_provider

    # Mock behavior for always invalid speech data
    llm_content_product = MagicMock()
    invalid_speech_data_product = MagicMock()
    invalid_speech_data_product.is_valid.return_value = False

    # Mock the content provider's generate_content method
    llm_content_provider = MagicMock()
    llm_content_provider.generate_content.return_value = llm_content_product
    llm_content_provider_factory.create_llm_content_provider.return_value = llm_content_provider

    # Mock the strategy's do_algorithm method to always return invalid speech data
    process_llm_content_strategy.do_algorithm.return_value = invalid_speech_data_product

    # Call the method under test
    speech_data = provider.create_speech_data()

    # Verify that the invalid speech data was returned after max retries
    assert not speech_data.is_valid()

    # Verify that the strategy and content provider were called the number of times defined by MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL
    assert llm_content_provider.generate_content.call_count == MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL
    assert process_llm_content_strategy.do_algorithm.call_count == MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL


def test_logging_on_invalid_speech_data(setup_llm_speech_data_provider, caplog):
    provider, _, llm_content_provider_factory, process_llm_content_strategy = setup_llm_speech_data_provider

    # Mock behavior for invalid speech data
    llm_content_product = MagicMock()
    invalid_speech_data_product = MagicMock()
    invalid_speech_data_product.is_valid.return_value = False
    invalid_speech_data_product.get_error.return_value = "Error message"

    # Mock the content provider's generate_content method
    llm_content_provider = MagicMock()
    llm_content_provider.generate_content.return_value = llm_content_product
    llm_content_provider_factory.create_llm_content_provider.return_value = llm_content_provider

    # Mock the strategy's do_algorithm method to always return invalid speech data
    process_llm_content_strategy.do_algorithm.return_value = invalid_speech_data_product

    # Call the method under test
    provider.create_speech_data()

    # Verify that error messages are logged for each invalid speech data
    assert "Failed to produce valid speech data: Error message" in caplog.text
