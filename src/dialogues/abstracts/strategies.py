from abc import abstractmethod, ABC
from typing import List

from src.dialogues.abstracts.factory_products import PlayerInputProduct, SpeechDataProduct
from src.prompting.abstracts.factory_products import LlmToolResponseProduct, LlmContentProduct


class InvolvePlayerInDialogueStrategy(ABC):
    @abstractmethod
    def do_algorithm(self, previous_messages: List[dict], dialogue: List[str]) -> PlayerInputProduct:
        pass


class DetermineUserMessagesForSpeechTurnStrategy(ABC):
    @abstractmethod
    def do_algorithm(self, speech_turn_tool_response_product: LlmToolResponseProduct):
        pass


class DetermineSystemMessageForSpeechTurnStrategy(ABC):
    @abstractmethod
    def do_algorithm(self, speech_turn_tool_response_product: LlmToolResponseProduct):
        pass


class ProcessLlmContentIntoSpeechDataStrategy(ABC):
    @abstractmethod
    def do_algorithm(self, llm_content_product: LlmContentProduct) -> SpeechDataProduct:
        pass
