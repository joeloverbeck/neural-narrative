import logging
from typing import List, Optional

from src.base.abstracts.observer import Observer
from src.base.playthrough_manager import PlaythroughManager
from src.dialogues.abstracts.abstract_factories import DialogueTurnFactorySubject
from src.dialogues.abstracts.factory_products import DialogueProduct, PlayerInputProduct
from src.dialogues.configs.dialogue_turn_factory_config import DialogueTurnFactoryConfig
from src.dialogues.configs.dialogue_turn_factory_factories_config import (
    DialogueTurnFactoryFactoriesConfig,
)
from src.dialogues.configs.dialogue_turn_factory_strategies_config import (
    DialogueTurnFactoryStrategiesConfig,
)
from src.dialogues.exceptions import InvalidNextSpeakerError, DialogueProcessingError
from src.dialogues.products.concrete_dialogue_product import ConcreteDialogueProduct
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)

logger = logging.getLogger(__name__)


class ConcreteDialogueTurnFactory(DialogueTurnFactorySubject):

    def __init__(
        self,
        dialogue_turn_factory_config: DialogueTurnFactoryConfig,
        dialogue_turn_factory_factories_config: DialogueTurnFactoryFactoriesConfig,
        dialogue_turn_factory_strategies_config: DialogueTurnFactoryStrategiesConfig,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        self._config = dialogue_turn_factory_config
        self._factories_config = dialogue_turn_factory_factories_config
        self._strategies_config = dialogue_turn_factory_strategies_config

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._config.playthrough_name
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
        return self._strategies_config.involve_player_in_dialogue_strategy.do_algorithm(
            self._config.transcription
        )

    def _choose_next_speaker(self) -> LlmToolResponseProduct:
        """Determine the next speaker in the dialogue."""
        response_provider = self._factories_config.speech_turn_choice_tool_response_provider_factory.create_speech_turn_choice_tool_response_provider(
            self._config.transcription
        )
        response_product = response_provider.generate_product()

        if not response_product.is_valid():
            raise InvalidNextSpeakerError(response_product.get_error())

        return response_product

    def _validate_next_speaker(
        self, speech_turn_choice_response: LlmToolResponseProduct
    ) -> None:
        """Validate that the next speaker is not the player."""
        if "voice_model" not in speech_turn_choice_response.get():
            raise ValueError("voice_model can't be empty.")
        if (
            speech_turn_choice_response.get()["identifier"]
            == self._playthrough_manager.get_player_identifier()
        ):
            raise InvalidNextSpeakerError("Next speaker cannot be the player.")

    def _process_speech_turn(
        self,
        player_input_product: PlayerInputProduct,
        speech_turn_choice_response: LlmToolResponseProduct,
    ):
        """Process the speech turn for the given speaker."""

        if "voice_model" not in speech_turn_choice_response.get():
            raise ValueError("voice_model can't be empty.")

        command = self._factories_config.create_speech_turn_data_command_factory.create_command(
            speech_turn_choice_response
        )

        for observer in self._observers:
            command.attach(observer)

        command.execute()

    def _create_dialogue_product(self, has_ended: bool) -> DialogueProduct:
        """Create a dialogue product indicating whether the dialogue has ended."""
        return ConcreteDialogueProduct(
            self._config.transcription,
            has_ended=has_ended,
        )

    def _determine_next_speaker(self) -> LlmToolResponseProduct:
        if not self._config.participants.has_only_two_participants_with_player(
            self._playthrough_manager.get_player_identifier()
        ):
            return self._choose_next_speaker()
        else:
            return ConcreteLlmToolResponseProduct(
                self._config.participants.get_other_participant_data(
                    self._playthrough_manager.get_player_identifier()
                ),
                is_valid=True,
            )

    def process_turn_of_dialogue(self) -> DialogueProduct:
        try:
            player_input_product = self._get_player_input()
            if player_input_product.is_goodbye():
                return self._create_dialogue_product(has_ended=True)
            speech_turn_choice_response = self._determine_next_speaker()
            self._validate_next_speaker(speech_turn_choice_response)
            self._process_speech_turn(player_input_product, speech_turn_choice_response)
            return self._create_dialogue_product(has_ended=False)
        except DialogueProcessingError as e:
            logger.error("Error processing dialogue turn: %s", e)
            raise
        except FileNotFoundError as e:
            raise DialogueProcessingError(
                "Was unable to find a file. Error: %s", e
            ) from e
        except Exception as e:
            raise DialogueProcessingError("An unexpected error occurred: %s", e) from e
