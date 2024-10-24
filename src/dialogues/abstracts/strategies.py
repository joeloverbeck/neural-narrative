from abc import abstractmethod, ABC
from typing import Protocol, List

from src.characters.character import Character
from src.dialogues.abstracts.factory_products import (
    PlayerInputProduct,
    SpeechDataProduct,
)
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import (
    LlmToolResponseProduct,
    LlmContentProduct,
)


class InvolvePlayerInDialogueStrategy(Protocol):

    def do_algorithm(self, transcription: Transcription) -> PlayerInputProduct:
        pass


class ProcessLlmContentIntoSpeechDataStrategy(ABC):

    @abstractmethod
    def do_algorithm(self, llm_content_product: LlmContentProduct) -> SpeechDataProduct:
        pass


class MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(Protocol):

    def produce_message_data(
        self, player_character: Character, player_input_product: PlayerInputProduct
    ) -> dict:
        pass


class MessageDataProducerForSpeechTurnStrategy(Protocol):

    def produce_message_data(
        self,
        speech_turn_choice_tool_response_product: LlmToolResponseProduct,
        speech_data_product: SpeechDataProduct,
    ) -> dict[str, str]:
        pass


class ChooseParticipantsStrategy(Protocol):

    def choose_participants(self) -> List[str]:
        pass
