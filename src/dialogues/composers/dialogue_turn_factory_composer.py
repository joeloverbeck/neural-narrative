from typing import Optional

from src.config.config_manager import ConfigManager
from src.dialogues.abstracts.abstract_factories import DialogueTurnFactorySubject
from src.dialogues.abstracts.strategies import InvolvePlayerInDialogueStrategy, MessageDataProducerForSpeechTurnStrategy
from src.dialogues.composers.determine_system_message_for_speech_turn_strategy_composer import \
    DetermineSystemMessageForSpeechTurnStrategyComposer
from src.dialogues.composers.llm_speech_data_provider_factory_composer import LlmSpeechDataProviderFactoryComposer
from src.dialogues.composers.speech_turn_choice_tool_response_factory_composer import \
    SpeechTurnChoiceToolResponseFactoryComposer
from src.dialogues.configs.dialogue_turn_factory_config import DialogueTurnFactoryConfig
from src.dialogues.configs.dialogue_turn_factory_factories_config import DialogueTurnFactoryFactoriesConfig
from src.dialogues.configs.dialogue_turn_factory_strategies_config import DialogueTurnFactoryStrategiesConfig
from src.dialogues.factories.concrete_dialogue_turn_factory import ConcreteDialogueTurnFactory
from src.dialogues.factories.create_speech_turn_data_command_factory import CreateSpeechTurnDataCommandFactory
from src.dialogues.factories.determine_user_messages_for_speech_turn_strategy_factory import \
    DetermineUserMessagesForSpeechTurnStrategyFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.llm_client import LlmClient


class DialogueTurnFactoryComposer:

    def __init__(self, playthrough_name: str, player_identifier: str,
                 participants: Participants, purpose: Optional[str], llm_client:
            LlmClient, messages_to_llm: MessagesToLlm, transcription:
            Transcription, involve_player_in_dialogue_strategy:
            InvolvePlayerInDialogueStrategy,
                 message_data_producer_for_speech_turn_strategy:
                 MessageDataProducerForSpeechTurnStrategy):
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._purpose = purpose
        self._llm_client = llm_client
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._involve_player_in_dialogue_strategy = (
            involve_player_in_dialogue_strategy)
        self._message_data_producer_for_speech_turn_strategy = (
            message_data_producer_for_speech_turn_strategy)

    def compose(self) -> DialogueTurnFactorySubject:
        speech_turn_choice_tool_response_provider_factory = (
            SpeechTurnChoiceToolResponseFactoryComposer(self.
                                                        _playthrough_name, self._player_identifier, self._participants,
                                                        self._llm_client, ConfigManager().get_light_llm()).compose())
        llm_speech_data_provider_factory = (
            LlmSpeechDataProviderFactoryComposer(self._llm_client,
                                                 ConfigManager().get_heavy_llm()).compose())
        determine_system_message_for_speech_turn_strategy = (
            DetermineSystemMessageForSpeechTurnStrategyComposer(self.
                                                                _playthrough_name, self._participants, self._purpose,
                                                                self.
                                                                _messages_to_llm).compose())
        determine_user_messages_for_speech_turn_strategy_factory = (
            DetermineUserMessagesForSpeechTurnStrategyFactory(self.
                                                              _playthrough_name, self._player_identifier))
        create_speech_turn_data_command_factory = (
            CreateSpeechTurnDataCommandFactory(self._messages_to_llm, self.
                                               _transcription, llm_speech_data_provider_factory, self.
                                               _message_data_producer_for_speech_turn_strategy))
        return ConcreteDialogueTurnFactory(DialogueTurnFactoryConfig(self.
                                                                     _playthrough_name, self._participants,
                                                                     self._messages_to_llm,
                                                                     self._transcription),
                                           DialogueTurnFactoryFactoriesConfig(
                                               speech_turn_choice_tool_response_provider_factory,
                                               create_speech_turn_data_command_factory,
                                               determine_user_messages_for_speech_turn_strategy_factory),
                                           DialogueTurnFactoryStrategiesConfig(self.
                                                                               _involve_player_in_dialogue_strategy,
                                                                               determine_system_message_for_speech_turn_strategy))
