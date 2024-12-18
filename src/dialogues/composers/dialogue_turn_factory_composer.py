from typing import Optional, List

from src.base.abstracts.observer import Observer
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.abstract_factories import (
    DialogueTurnFactorySubject,
    PlayerInputFactory,
)
from src.dialogues.algorithms.determine_next_speaker_algorithm import (
    DetermineNextSpeakerAlgorithm,
)
from src.dialogues.composers.llm_speech_data_provider_factory_composer import (
    LlmSpeechDataProviderFactoryComposer,
)
from src.dialogues.composers.load_or_initialize_dialogue_data_command_factory_composer import (
    LoadOrInitializeDialogueDataCommandFactoryComposer,
)
from src.dialogues.composers.speech_turn_choice_tool_response_factory_composer import (
    SpeechTurnChoiceToolResponseFactoryComposer,
)
from src.dialogues.configs.dialogue_turn_factory_config import DialogueTurnFactoryConfig
from src.dialogues.configs.dialogue_turn_factory_factories_config import (
    DialogueTurnFactoryFactoriesConfig,
)
from src.dialogues.configs.dialogue_turn_factory_strategies_config import (
    DialogueTurnFactoryStrategiesConfig,
)
from src.dialogues.factories.concrete_dialogue_turn_factory import (
    ConcreteDialogueTurnFactory,
)
from src.dialogues.factories.create_speech_turn_data_command_factory import (
    CreateSpeechTurnDataCommandFactory,
)
from src.dialogues.factories.introduce_player_input_into_dialogue_command_factory import (
    IntroducePlayerInputIntoDialogueCommandFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.strategies.concrete_involve_player_in_dialogue_strategy import (
    ConcreteInvolvePlayerInDialogueStrategy,
)
from src.dialogues.strategies.web_message_data_producer_for_introduce_player_input_into_dialogue_strategy import (
    WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)
from src.dialogues.strategies.web_message_data_producer_for_speech_turn_strategy import (
    WebMessageDataProducerForSpeechTurnStrategy,
)
from src.dialogues.transcription import Transcription


class DialogueTurnFactoryComposer:

    def __init__(
        self,
        playthrough_name: str,
        other_characters_identifiers: List[str],
        participants: Participants,
        purpose: Optional[str],
        dialogue_observer: Observer,
        player_input_factory: PlayerInputFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._other_characters_identifiers = other_characters_identifiers
        self._participants = participants
        self._purpose = purpose
        self._dialogue_observer = dialogue_observer
        self._player_input_factory = player_input_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def compose(self) -> DialogueTurnFactorySubject:
        player_identifier = self._playthrough_manager.get_player_identifier()

        message_data_producer_for_introduce_player_input_into_dialogue_strategy = (
            WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy()
        )

        introduce_player_input_into_dialogue_command_factory = (
            IntroducePlayerInputIntoDialogueCommandFactory(
                self._playthrough_name,
                player_identifier,
                message_data_producer_for_introduce_player_input_into_dialogue_strategy,
            )
        )

        involve_player_in_dialogue_strategy = ConcreteInvolvePlayerInDialogueStrategy(
            player_identifier,
            self._player_input_factory,
            introduce_player_input_into_dialogue_command_factory,
        )

        involve_player_in_dialogue_strategy.attach(self._dialogue_observer)

        speech_turn_choice_tool_response_provider_factory = (
            SpeechTurnChoiceToolResponseFactoryComposer(
                self._playthrough_name, player_identifier, self._participants
            ).compose()
        )

        transcription = Transcription()

        load_ongoing_conversation_data_command_factory = (
            LoadOrInitializeDialogueDataCommandFactoryComposer(
                self._playthrough_name,
                self._other_characters_identifiers,
                self._participants,
            ).compose_factory()
        )

        load_ongoing_conversation_data_command_factory.create_command(
            transcription
        ).execute()

        llm_speech_data_provider_factory = LlmSpeechDataProviderFactoryComposer(
            self._playthrough_name, self._participants, self._purpose
        ).compose()

        message_data_producer_for_speech_turn_strategy = (
            WebMessageDataProducerForSpeechTurnStrategy(
                self._playthrough_name,
                player_identifier,
            )
        )

        determine_next_speaker_algorithm = DetermineNextSpeakerAlgorithm(
            self._playthrough_name,
            self._participants,
            transcription,
            speech_turn_choice_tool_response_provider_factory,
        )

        create_speech_turn_data_command_factory = CreateSpeechTurnDataCommandFactory(
            transcription,
            llm_speech_data_provider_factory,
            message_data_producer_for_speech_turn_strategy,
        )

        dialogue_turn_factory = ConcreteDialogueTurnFactory(
            DialogueTurnFactoryConfig(
                self._playthrough_name,
                transcription,
            ),
            DialogueTurnFactoryFactoriesConfig(
                create_speech_turn_data_command_factory,
            ),
            DialogueTurnFactoryStrategiesConfig(
                involve_player_in_dialogue_strategy,
                determine_next_speaker_algorithm,
            ),
        )

        dialogue_turn_factory.attach(self._dialogue_observer)

        return dialogue_turn_factory
