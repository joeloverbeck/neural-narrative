from src.dialogues.factories.process_llm_content_into_speech_data_strategy_factory import \
    ProcessLlmContentIntoSpeechDataStrategyFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.providers.llm_speech_data_provider import LlmSpeechDataProvider
from src.prompting.factories.llm_content_provider_factory import LlmContentProviderFactory


class LlmSpeechDataProviderFactory:

    def __init__(self, llm_content_provider_factory:
    LlmContentProviderFactory,
                 process_llm_content_into_speech_data_strategy_factory:
                 ProcessLlmContentIntoSpeechDataStrategyFactory):
        self._llm_content_provider_factory = llm_content_provider_factory
        self._process_llm_content_into_speech_data_strategy_factory = (
            process_llm_content_into_speech_data_strategy_factory)

    def create_llm_speech_data_provider(self, messages_to_llm: MessagesToLlm
                                        ) -> LlmSpeechDataProvider:
        return LlmSpeechDataProvider(messages_to_llm, self.
                                     _llm_content_provider_factory, self.
                                     _process_llm_content_into_speech_data_strategy_factory.
                                     create_process_llm_content_into_speech_data_strategy(
            messages_to_llm))
