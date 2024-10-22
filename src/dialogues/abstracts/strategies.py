from abc import abstractmethod, ABC
from typing import Protocol, List
from src.characters.character import Character
from src.dialogues.abstracts.factory_products import (
    PlayerInputProduct,
    SpeechDataProduct,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import (
    LlmToolResponseProduct,
    LlmContentProduct,
)


class InvolvePlayerInDialogueStrategy(Protocol):

    def do_algorithm(
        self, messages_to_llm: MessagesToLlm, transcription: Transcription
    ) -> PlayerInputProduct:
        pass


class DetermineUserMessagesForSpeechTurnStrategy(ABC):

    @abstractmethod
    def do_algorithm(self, speech_turn_tool_response_product: LlmToolResponseProduct):
        pass


class DetermineSystemMessageForSpeechTurnStrategy(ABC):

    @abstractmethod
    def do_algorithm(
        self, speech_turn_choice_tool_response_product: LlmToolResponseProduct
    ):
        pass


class ProcessLlmContentIntoSpeechDataStrategy(ABC):

    @abstractmethod
    def do_algorithm(self, llm_content_product: LlmContentProduct) -> SpeechDataProduct:
        pass


class PromptFormatterForDialogueStrategy(ABC):

    @abstractmethod
    def do_algorithm(self) -> str:
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
