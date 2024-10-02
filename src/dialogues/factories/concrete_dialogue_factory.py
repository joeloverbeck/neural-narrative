from typing import Optional, List

from src.abstracts.observer import Observer
from src.dialogues.abstracts.abstract_factories import (
    DialogueFactorySubject,
)
from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.abstracts.strategies import (
    InvolvePlayerInDialogueStrategy,
    DetermineSystemMessageForSpeechTurnStrategy,
)
from src.dialogues.factories.create_speech_turn_data_command_factory import (
    CreateSpeechTurnDataCommandFactory,
)
from src.dialogues.factories.determine_user_messages_for_speech_turn_strategy_factory import (
    DetermineUserMessagesForSpeechTurnStrategyFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.products.concrete_dialogue_product import ConcreteDialogueProduct
from src.dialogues.transcription import Transcription
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import (
    SpeechTurnChoiceToolResponseProviderFactory,
)
from tests.test_concrete_llm_content_factory import messages_to_llm


class ConcreteDialogueFactory(DialogueFactorySubject):
    def __init__(
        self,
        playthrough_name: str,
        messages_to_llm: Optional[MessagesToLlm],
        transcription: Optional[Transcription],
        involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategy,
        speech_turn_choice_tool_response_provider_factory: SpeechTurnChoiceToolResponseProviderFactory,
        determine_system_message_for_speech_turn_strategy: DetermineSystemMessageForSpeechTurnStrategy,
        determine_user_messages_for_speech_turn_strategy_factory: DetermineUserMessagesForSpeechTurnStrategyFactory,
        create_speech_turn_data_command_factory: CreateSpeechTurnDataCommandFactory,
        playthrough_manager: PlaythroughManager = None,
    ):
        self._playthrough_name = playthrough_name
        self._involve_player_in_dialogue_strategy = involve_player_in_dialogue_strategy
        self._speech_turn_choice_tool_response_provider_factory = (
            speech_turn_choice_tool_response_provider_factory
        )
        self._determine_system_message_for_speech_turn_strategy = (
            determine_system_message_for_speech_turn_strategy
        )
        self._determine_user_messages_for_speech_turn_strategy_factory = (
            determine_user_messages_for_speech_turn_strategy_factory
        )

        self._messages_to_llm = messages_to_llm or MessagesToLlm()
        self._transcription = transcription or Transcription()

        self._create_speech_turn_data_command_factory = (
            create_speech_turn_data_command_factory
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def process_turn_of_dialogue(self) -> DialogueProduct:
        player_input_product = self._involve_player_in_dialogue_strategy.do_algorithm(
            self._messages_to_llm, self._transcription
        )

        if player_input_product.is_goodbye():
            return ConcreteDialogueProduct(
                self._messages_to_llm, self._transcription, has_ended=True
            )

        speech_turn_choice_tool_response_product = self._speech_turn_choice_tool_response_provider_factory.create_speech_turn_choice_tool_response_provider(
            self._transcription
        ).create_llm_response()

        if not speech_turn_choice_tool_response_product.is_valid():
            raise ValueError(
                f"Was unable to choose next speaker: {speech_turn_choice_tool_response_product.get_error()}"
            )

        # If at this point the speech turn choice is still the player, we have a problem, because the previous code
        # should have effectively blocked that possibility.
        if (
            speech_turn_choice_tool_response_product.get()["identifier"]
            == self._playthrough_manager.get_player_identifier()
        ):
            raise ValueError(
                "Was about to produce the speech turn, but the player had been chosen as the next speaker."
            )

        # Proceed with the rest of the processing
        self._determine_system_message_for_speech_turn_strategy.do_algorithm(
            speech_turn_choice_tool_response_product
        )
        self._determine_user_messages_for_speech_turn_strategy_factory.create_determine_user_messages_for_speech_turn_strategy(
            player_input_product, self._messages_to_llm
        ).do_algorithm(
            speech_turn_choice_tool_response_product
        )

        create_speech_turn_data_command = (
            self._create_speech_turn_data_command_factory.create_command(
                speech_turn_choice_tool_response_product
            )
        )

        for observer in self._observers:
            create_speech_turn_data_command.attach(observer)

        create_speech_turn_data_command.execute()

        return ConcreteDialogueProduct(
            self._messages_to_llm, self._transcription, has_ended=False
        )
