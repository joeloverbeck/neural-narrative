from src.dialogues.factories.llm_speech_data_provider_factory import LlmSpeechDataProviderFactory
from src.dialogues.factories.process_llm_content_into_speech_data_strategy_factory import \
    ProcessLlmContentIntoSpeechDataStrategyFactory
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.factories.llm_content_provider_factory import LlmContentProviderFactory
from src.prompting.factories.speech_tool_response_data_extraction_provider_factory import \
    SpeechToolResponseDataExtractionProviderFactory
from src.prompting.factories.tool_response_parsing_provider_factory import ToolResponseParsingProviderFactory


class LlmSpeechDataProviderFactoryComposer:

    def __init__(self, llm_client: LlmClient, model: str):
        self._llm_client = llm_client
        self._model = model

    def compose(self) -> LlmSpeechDataProviderFactory:
        tool_response_parsing_provider_factory = (
            ToolResponseParsingProviderFactory())
        speech_tool_response_data_extraction_provider_factory = (
            SpeechToolResponseDataExtractionProviderFactory())
        process_llm_content_into_speech_data_strategy_factory = (
            ProcessLlmContentIntoSpeechDataStrategyFactory(
                tool_response_parsing_provider_factory,
                speech_tool_response_data_extraction_provider_factory))
        return LlmSpeechDataProviderFactory(LlmContentProviderFactory(self.
                                                                      _llm_client, self._model),
                                            process_llm_content_into_speech_data_strategy_factory)
