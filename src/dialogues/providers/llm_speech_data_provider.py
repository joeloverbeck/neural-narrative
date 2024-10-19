import logging

from src.base.constants import MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL
from src.dialogues.abstracts.abstract_factories import SpeechDataFactory
from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.abstracts.strategies import ProcessLlmContentIntoSpeechDataStrategy
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.products.concrete_speech_data_product import ConcreteSpeechDataProduct
from src.prompting.factories.llm_content_provider_factory import LlmContentProviderFactory

logger = logging.getLogger(__name__)


class LlmSpeechDataProvider(SpeechDataFactory):

    def __init__(self, messages_to_llm: MessagesToLlm,
                 llm_content_provider_factory: LlmContentProviderFactory,
                 process_llm_content_into_speech_data_strategy: ProcessLlmContentIntoSpeechDataStrategy):
        assert process_llm_content_into_speech_data_strategy

        self._messages_to_llm = messages_to_llm
        self._llm_content_provider_factory = llm_content_provider_factory
        self._process_llm_content_into_speech_data_strategy = process_llm_content_into_speech_data_strategy

        self._max_retries = MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL

    def create_speech_data(self) -> SpeechDataProduct:
        while self._max_retries > 0:
            llm_content_product = self._llm_content_provider_factory.create_llm_content_provider(
                self._messages_to_llm).generate_content()

            speech_data_product = self._process_llm_content_into_speech_data_strategy.do_algorithm(llm_content_product)

            if speech_data_product.is_valid():
                return speech_data_product

            # from this point on, the responses are invalid.
            self._max_retries -= 1
            logger.error(f"Failed to produce valid speech data: {speech_data_product.get_error()}")

        return ConcreteSpeechDataProduct({}, is_valid=False,
                                         error=f"Exhausted all retries when trying to get a valid response out of the LLM.")
