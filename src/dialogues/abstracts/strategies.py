from abc import abstractmethod, ABC
from typing import List, Any

from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class InvolvePlayerInDialogueStrategy(ABC):
    @abstractmethod
    def do_algorithm(self, previous_messages: List[dict], dialogue: List[dict[Any, str]]) -> PlayerInputProduct:
        pass


class DetermineUserMessagesForSpeechTurnStrategy(ABC):
    @abstractmethod
    def do_algorithm(self, speech_turn_tool_response_product: LlmToolResponseProduct):
        pass


class DetermineSystemMessageForSpeechTurnStrategy(ABC):
    @abstractmethod
    def do_algorithm(self, speech_turn_tool_response_product: LlmToolResponseProduct):
        pass
