import logging
from typing import List, Optional

from src.base.abstracts.observer import Observer
from src.base.playthrough_manager import PlaythroughManager
from src.base.tools import capture_traceback
from src.dialogues.abstracts.abstract_factories import DialogueTurnFactorySubject
from src.dialogues.abstracts.factory_products import DialogueProduct, PlayerInputProduct
from src.dialogues.configs.dialogue_turn_factory_config import DialogueTurnFactoryConfig
from src.dialogues.configs.dialogue_turn_factory_factories_config import (
    DialogueTurnFactoryFactoriesConfig,
)
from src.dialogues.configs.dialogue_turn_factory_strategies_config import (
    DialogueTurnFactoryStrategiesConfig,
)
from src.dialogues.exceptions import DialogueProcessingError
from src.dialogues.products.concrete_dialogue_product import ConcreteDialogueProduct
from src.prompting.abstracts.factory_products import LlmToolResponseProduct

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

    def _process_speech_turn(
        self,
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

    def process_turn_of_dialogue(self) -> DialogueProduct:
        try:
            player_input_product = self._get_player_input()

            if player_input_product.is_goodbye():
                return self._create_dialogue_product(has_ended=True)

            speech_turn_choice_response = (
                self._strategies_config.determine_next_speaker_algorithm.do_algorithm()
            )

            self._process_speech_turn(speech_turn_choice_response)

            return self._create_dialogue_product(has_ended=False)
        except DialogueProcessingError as e:
            logger.error("Error processing dialogue turn: %s", e)
            raise
        except FileNotFoundError as e:
            raise DialogueProcessingError(
                "Was unable to find a file. Error: %s", e
            ) from e
        except Exception as e:
            capture_traceback()
            raise DialogueProcessingError("An unexpected error occurred: %s", e) from e
