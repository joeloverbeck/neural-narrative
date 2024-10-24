from typing import Optional

from src.base.playthrough_manager import PlaythroughManager
from src.characters.factories.character_factory import CharacterFactory
from src.dialogues.abstracts.abstract_factories import DialogueTurnFactorySubject
from src.dialogues.abstracts.strategies import (
    InvolvePlayerInDialogueStrategy,
    MessageDataProducerForSpeechTurnStrategy,
)
from src.dialogues.composers.llm_speech_data_provider_factory_composer import (
    LlmSpeechDataProviderFactoryComposer,
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
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.llm_client import LlmClient


class DialogueTurnFactoryComposer:

    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        participants: Participants,
        purpose: Optional[str],
        llm_client: LlmClient,
        transcription: Transcription,
        involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategy,
        message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
    ):
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._purpose = purpose
        self._llm_client = llm_client
        self._transcription = transcription
        self._involve_player_in_dialogue_strategy = involve_player_in_dialogue_strategy
        self._message_data_producer_for_speech_turn_strategy = (
            message_data_producer_for_speech_turn_strategy
        )

    def compose(self) -> DialogueTurnFactorySubject:
        speech_turn_choice_tool_response_provider_factory = (
            SpeechTurnChoiceToolResponseFactoryComposer(
                self._playthrough_name, self._player_identifier, self._participants
            ).compose()
        )
        llm_speech_data_provider_factory = LlmSpeechDataProviderFactoryComposer(
            self._playthrough_name, self._participants, self._purpose
        ).compose()
        create_speech_turn_data_command_factory = CreateSpeechTurnDataCommandFactory(
            self._transcription,
            llm_speech_data_provider_factory,
            self._message_data_producer_for_speech_turn_strategy,
        )

        character_factory = CharacterFactory(self._playthrough_name)

        return ConcreteDialogueTurnFactory(
            DialogueTurnFactoryConfig(
                self._playthrough_name,
                PlaythroughManager(self._playthrough_name).get_player_identifier(),
                self._participants,
                self._transcription,
            ),
            DialogueTurnFactoryFactoriesConfig(
                character_factory,
                speech_turn_choice_tool_response_provider_factory,
                create_speech_turn_data_command_factory,
            ),
            DialogueTurnFactoryStrategiesConfig(
                self._involve_player_in_dialogue_strategy
            ),
        )
