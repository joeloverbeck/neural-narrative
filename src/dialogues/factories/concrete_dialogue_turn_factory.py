import logging
from typing import List, Optional, Dict

from src.base.abstracts.observer import Observer
from src.base.playthrough_manager import PlaythroughManager
from src.base.products.dict_product import DictProduct
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
from src.dialogues.models.summary_note import get_custom_summary_note_class
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
        summary_notes: dict[str, dict[str, str]],
    ):
        """Process the speech turn for the given speaker."""
        if "voice_model" not in speech_turn_choice_response.get():
            raise ValueError("voice_model can't be empty.")

        command = self._factories_config.create_speech_turn_data_command_factory.create_command(
            speech_turn_choice_response, summary_notes
        )

        for observer in self._observers:
            command.attach(observer)

        command.execute()

    def _create_dialogue_product(
        self,
        has_ended: bool,
        summary_notes: Optional[Dict[str, Dict[str, Dict[str, str]]]] = None,
    ) -> DialogueProduct:
        """Create a dialogue product indicating whether the dialogue has ended."""
        summary_notes_to_return = (
            summary_notes if summary_notes else self._config.summary_notes
        )

        return ConcreteDialogueProduct(
            self._config.transcription,
            summary_notes_to_return,
            has_ended=has_ended,
        )

    def _handle_player_input(self) -> Optional[DialogueProduct]:
        player_input_product = self._get_player_input()

        if player_input_product.is_goodbye():
            return self._create_dialogue_product(has_ended=True)

        return None

    def _create_summary_note(self, speaker_name: str) -> DictProduct:
        summary_note_provider = (
            self._factories_config.summary_note_provider_factory.create_provider(
                self._config.transcription, speaker_name
            )
        )

        return summary_note_provider.generate_product(
            get_custom_summary_note_class(speaker_name)
        )

    def _update_summary_notes(
        self, speaker_identifier: str, summary_note: Dict[str, Dict[str, str]]
    ) -> Dict[str, Dict[str, Dict[str, str]]]:
        update_algorithm = self._factories_config.update_summary_notes_algorithm_factory.create_algorithm(
            speaker_identifier,
            summary_note,
        )
        return update_algorithm.do_algorithm()

    def process_turn_of_dialogue(self) -> DialogueProduct:
        try:
            dialogue_product = self._handle_player_input()
            if dialogue_product:
                return dialogue_product

            speech_turn_choice_response = (
                self._strategies_config.determine_next_speaker_algorithm.do_algorithm()
            )

            # Must delegate creating the summary note.
            speaker_name = speech_turn_choice_response.get()["name"]

            summary_note_product = self._create_summary_note(speaker_name)

            # Note that the product is a DictProduct, not a TextsProduct as usual.
            self._process_speech_turn(
                speech_turn_choice_response, summary_note_product.get()
            )

            updated_summary_notes = self._update_summary_notes(
                speech_turn_choice_response.get()["identifier"],
                summary_note_product.get(),
            )

            return self._create_dialogue_product(
                has_ended=False, summary_notes=updated_summary_notes
            )
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
