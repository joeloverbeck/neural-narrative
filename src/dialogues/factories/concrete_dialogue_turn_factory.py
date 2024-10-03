import logging
from typing import List

from src.abstracts.observer import Observer
from src.dialogues.abstracts.abstract_factories import (
    DialogueTurnFactorySubject,
)
from src.dialogues.abstracts.factory_products import DialogueProduct, PlayerInputProduct
from src.dialogues.configs.dialogue_turn_factory_config import DialogueTurnFactoryConfig
from src.dialogues.configs.dialogue_turn_factory_factories_config import (
    DialogueTurnFactoryFactoriesConfig,
)
from src.dialogues.configs.dialogue_turn_factory_strategies_config import (
    DialogueTurnFactoryStrategiesConfig,
)
from src.dialogues.exceptions import InvalidNextSpeakerError, DialogueProcessingError
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.products.concrete_dialogue_product import ConcreteDialogueProduct
from src.dialogues.transcription import Transcription
from src.playthrough_manager import PlaythroughManager
from src.prompting.abstracts.factory_products import LlmToolResponseProduct

logger = logging.getLogger(__name__)


class ConcreteDialogueTurnFactory(DialogueTurnFactorySubject):
    def __init__(
        self,
            dialogue_turn_factory_config: DialogueTurnFactoryConfig,
            dialogue_turn_factory_factories_config: DialogueTurnFactoryFactoriesConfig,
            dialogue_turn_factory_strategies_config: DialogueTurnFactoryStrategiesConfig,
        playthrough_manager: PlaythroughManager = None,
    ):
        self._playthrough_name = dialogue_turn_factory_config.playthrough_name
        self._involve_player_in_dialogue_strategy = (
            dialogue_turn_factory_strategies_config.involve_player_in_dialogue_strategy
        )
        self._speech_turn_choice_tool_response_provider_factory = (
            dialogue_turn_factory_factories_config.speech_turn_choice_tool_response_provider_factory
        )
        self._determine_system_message_for_speech_turn_strategy = (
            dialogue_turn_factory_strategies_config.determine_system_message_for_speech_turn_strategy
        )
        self._determine_user_messages_for_speech_turn_strategy_factory = (
            dialogue_turn_factory_factories_config.determine_user_messages_for_speech_turn_strategy_factory
        )

        self._messages_to_llm = (
                dialogue_turn_factory_config.messages_to_llm or MessagesToLlm()
        )
        self._transcription = (
                dialogue_turn_factory_config.transcription or Transcription()
        )

        self._create_speech_turn_data_command_factory = (
            dialogue_turn_factory_factories_config.create_speech_turn_data_command_factory
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer to the dialogue turn factory."""
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def _get_player_input(self) -> PlayerInputProduct:
        """Retrieve and process player input."""
        return self._involve_player_in_dialogue_strategy.do_algorithm(
            self._messages_to_llm, self._transcription
        )

    def _choose_next_speaker(self) -> LlmToolResponseProduct:
        """Determine the next speaker in the dialogue."""
        response_provider = self._speech_turn_choice_tool_response_provider_factory.create_speech_turn_choice_tool_response_provider(
            self._transcription
        )

        response_product = response_provider.create_llm_response()

        if not response_product.is_valid():
            raise InvalidNextSpeakerError(response_product.get_error())

        return response_product

    def _validate_next_speaker(self, response_product: LlmToolResponseProduct) -> None:
        """Validate that the next speaker is not the player."""
        if (
                response_product.get()["identifier"]
            == self._playthrough_manager.get_player_identifier()
        ):
            raise InvalidNextSpeakerError("Next speaker cannot be the player.")

    def _process_speech_turn(
            self,
            player_input_product: PlayerInputProduct,
            response_product: LlmToolResponseProduct,
    ):
        """Process the speech turn for the given speaker."""
        self._determine_system_message_for_speech_turn_strategy.do_algorithm(
            response_product
        )

        user_messages_strategy = self._determine_user_messages_for_speech_turn_strategy_factory.create_strategy(
            player_input_product, self._messages_to_llm
        )

        user_messages_strategy.do_algorithm(response_product)

        command = self._create_speech_turn_data_command_factory.create_command(
            response_product
        )

        for observer in self._observers:
            command.attach(observer)

        command.execute()

    def _create_dialogue_product(self, has_ended: bool) -> DialogueProduct:
        """Create a dialogue product indicating whether the dialogue has ended."""
        return ConcreteDialogueProduct(
            self._messages_to_llm, self._transcription, has_ended=has_ended
        )

    def process_turn_of_dialogue(self) -> DialogueProduct:
        try:
            player_input_product = self._get_player_input()

            if player_input_product.is_goodbye():
                return self._create_dialogue_product(has_ended=True)

            speech_turn_choice_tool_response_product = self._choose_next_speaker()

            self._validate_next_speaker(speech_turn_choice_tool_response_product)

            self._process_speech_turn(
                player_input_product, speech_turn_choice_tool_response_product
            )

            return self._create_dialogue_product(has_ended=False)
        except DialogueProcessingError as e:
            # Handle specific dialogue processing errors
            logger.error("Error processing dialogue turn: %s", e)
            raise
        except Exception as e:
            # Handle unexpected exceptions
            raise DialogueProcessingError("An unexpected error occurred: %s", e) from e
