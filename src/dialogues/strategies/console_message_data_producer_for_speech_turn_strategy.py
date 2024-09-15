from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.abstracts.strategies import MessageDataProducerForSpeechTurnStrategy
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class ConsoleMessageDataProducerForSpeechTurnStrategy(MessageDataProducerForSpeechTurnStrategy):
    def produce_message_data(self, speech_turn_choice_tool_response_product: LlmToolResponseProduct,
                             speech_data_product: SpeechDataProduct) -> dict[str, str]:
        return speech_data_product.get()
