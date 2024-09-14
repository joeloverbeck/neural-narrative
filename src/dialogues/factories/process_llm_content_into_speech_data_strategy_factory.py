from src.dialogues.abstracts.strategies import ProcessLlmContentIntoSpeechDataStrategy
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.strategies.concrete_process_llm_content_into_speech_data_strategy import \
    ConcreteProcessLlmContentIntoSpeechDataStrategy
from src.prompting.factories.speech_tool_response_data_extraction_provider_factory import \
    SpeechToolResponseDataExtractionProviderFactory
from src.prompting.factories.tool_response_parsing_provider_factory import ToolResponseParsingProviderFactory


class ProcessLlmContentIntoSpeechDataStrategyFactory:

    def __init__(self, tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory,
                 speech_tool_response_data_extraction_provider_factory: SpeechToolResponseDataExtractionProviderFactory):
        self._tool_response_parsing_provider_factory = tool_response_parsing_provider_factory
        self._speech_tool_response_data_extraction_provider_factory = speech_tool_response_data_extraction_provider_factory

    def create_process_llm_content_into_speech_data_strategy(self,
                                                             messages_to_llm: MessagesToLlm) -> ProcessLlmContentIntoSpeechDataStrategy:
        return ConcreteProcessLlmContentIntoSpeechDataStrategy(messages_to_llm,
                                                               self._tool_response_parsing_provider_factory,
                                                               self._speech_tool_response_data_extraction_provider_factory)
