from src.constants import HERMES_405B, HERMES_70B
from src.dialogues.abstracts.abstract_factories import (
    DialogueFactorySubject,
)
from src.dialogues.abstracts.strategies import (
    InvolvePlayerInDialogueStrategy,
    MessageDataProducerForSpeechTurnStrategy,
)
from src.dialogues.composers.determine_system_message_for_speech_turn_strategy_composer import (
    DetermineSystemMessageForSpeechTurnStrategyComposer,
)
from src.dialogues.composers.llm_speech_data_provider_factory_composer import (
    LlmSpeechDataProviderFactoryComposer,
)
from src.dialogues.composers.speech_turn_choice_tool_response_factory_composer import (
    SpeechTurnChoiceToolResponseFactoryComposer,
)
from src.dialogues.factories.concrete_dialogue_factory import ConcreteDialogueFactory
from src.dialogues.factories.create_speech_turn_data_command_factory import (
    CreateSpeechTurnDataCommandFactory,
)
from src.dialogues.factories.determine_user_messages_for_speech_turn_strategy_factory import (
    DetermineUserMessagesForSpeechTurnStrategyFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.llm_client import LlmClient


class DialogueFactoryComposer:

    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        participants: Participants,
        llm_client: LlmClient,
        messages_to_llm: MessagesToLlm,
        transcription: Transcription,
        involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategy,
        message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not player_identifier:
            raise ValueError("player_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._llm_client = llm_client
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._involve_player_in_dialogue_strategy = involve_player_in_dialogue_strategy
        self._message_data_producer_for_speech_turn_strategy = (
            message_data_producer_for_speech_turn_strategy
        )

    def compose(self) -> DialogueFactorySubject:
        speech_turn_choice_tool_response_provider_factory = (
            SpeechTurnChoiceToolResponseFactoryComposer(
                self._playthrough_name,
                self._player_identifier,
                self._participants,
                self._llm_client,
                HERMES_70B,
            ).compose()
        )

        llm_speech_data_provider_factory = LlmSpeechDataProviderFactoryComposer(
            self._llm_client, HERMES_405B
        ).compose()

        determine_system_message_for_speech_turn_strategy = (
            DetermineSystemMessageForSpeechTurnStrategyComposer(
                self._playthrough_name, self._participants, self._messages_to_llm
            ).compose()
        )

        determine_user_messages_for_speech_turn_strategy_factory = (
            DetermineUserMessagesForSpeechTurnStrategyFactory(
                self._playthrough_name, self._player_identifier
            )
        )

        create_speech_turn_data_command_factory = CreateSpeechTurnDataCommandFactory(
            self._messages_to_llm,
            self._transcription,
            llm_speech_data_provider_factory,
            self._message_data_producer_for_speech_turn_strategy,
        )

        return ConcreteDialogueFactory(
            self._playthrough_name,
            self._messages_to_llm,
            self._transcription,
            self._involve_player_in_dialogue_strategy,
            speech_turn_choice_tool_response_provider_factory,
            determine_system_message_for_speech_turn_strategy,
            determine_user_messages_for_speech_turn_strategy_factory,
            create_speech_turn_data_command_factory,
        )
