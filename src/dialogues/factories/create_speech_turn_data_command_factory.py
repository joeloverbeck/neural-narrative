from src.dialogues.abstracts.strategies import MessageDataProducerForSpeechTurnStrategy
from src.dialogues.commands.create_speech_turn_data_command import (
    CreateSpeechTurnDataCommand,
)
from src.dialogues.factories.llm_speech_data_provider_factory import (
    LlmSpeechDataProviderFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from tests.test_concrete_llm_content_factory import messages_to_llm


class CreateSpeechTurnDataCommandFactory:

    def __init__(
        self,
        messages_to_llm: MessagesToLlm,
        transcription: Transcription,
        llm_speech_data_provider_factory: LlmSpeechDataProviderFactory,
        message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
    ):
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._llm_speech_data_provider_factory = llm_speech_data_provider_factory
        self._message_data_producer_for_speech_turn_strategy = (
            message_data_producer_for_speech_turn_strategy
        )

    def create_command(
        self, speech_turn_choice_tool_response_product: LlmToolResponseProduct
    ) -> CreateSpeechTurnDataCommand:
        return CreateSpeechTurnDataCommand(
            self._messages_to_llm,
            self._transcription,
            speech_turn_choice_tool_response_product,
            self._llm_speech_data_provider_factory,
            self._message_data_producer_for_speech_turn_strategy,
        )
