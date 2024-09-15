from typing import Optional

from src.abstracts.command import Command
from src.abstracts.observer import Observer
from src.constants import HERMES_70B, HERMES_405B
from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.strategies import MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy, \
    MessageDataProducerForSpeechTurnStrategy
from src.dialogues.composers.llm_speech_data_provider_factory_composer import LlmSpeechDataProviderFactoryComposer
from src.dialogues.composers.orchestrate_dialogue_production_command_composer import \
    OrchestrateDialogueProductionCommandComposer
from src.dialogues.composers.speech_turn_choice_tool_response_factory_composer import \
    SpeechTurnChoiceToolResponseFactoryComposer
from src.dialogues.composers.speech_turn_produce_messages_to_prompt_llm_command_factory_composer import \
    SpeechTurnProduceMessagesToPromptLlmCommandFactoryComposer
from src.dialogues.factories.concrete_dialogue_factory import ConcreteDialogueFactory
from src.dialogues.factories.introduce_player_input_into_dialogue_command_factory import \
    IntroducePlayerInputIntoDialogueCommandFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.strategies.concrete_involve_player_in_dialogue_strategy import \
    ConcreteInvolvePlayerInDialogueStrategy
from src.dialogues.transcription import Transcription
from src.prompting.factories.openrouter_llm_client_factory import OpenRouterLlmClientFactory


class LaunchDialogueCommand(Command):
    def __init__(self, playthrough_name: str, player_identifier: str, participants: Participants,
                 messages_to_llm: Optional[MessagesToLlm], transcription: Optional[Transcription],
                 dialogue_observer: Observer, player_input_factory: PlayerInputFactory,
                 message_data_producer_for_introduce_player_input_into_dialogue_strategy: MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
                 message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._dialogue_observer = dialogue_observer
        self._player_input_factory = player_input_factory
        self._message_data_producer_for_introduce_player_input_into_dialogue_strategy = message_data_producer_for_introduce_player_input_into_dialogue_strategy
        self._message_data_producer_for_speech_turn_strategy = message_data_producer_for_speech_turn_strategy

    def execute(self) -> None:

        introduce_player_input_into_dialogue_command_factory = IntroducePlayerInputIntoDialogueCommandFactory(
            self._playthrough_name, self._player_identifier,
            self._message_data_producer_for_introduce_player_input_into_dialogue_strategy)

        involve_player_in_dialogue_strategy = ConcreteInvolvePlayerInDialogueStrategy(self._player_identifier,
                                                                                      self._player_input_factory,
                                                                                      introduce_player_input_into_dialogue_command_factory)

        speech_turn_produce_messages_to_prompt_llm_command_factory = SpeechTurnProduceMessagesToPromptLlmCommandFactoryComposer(
            self._playthrough_name,
            self._player_identifier,
            self._participants).compose()

        llm_client = OpenRouterLlmClientFactory().create_llm_client()

        speech_turn_choice_tool_response_provider_factory = SpeechTurnChoiceToolResponseFactoryComposer(
            self._playthrough_name,
            self._player_identifier,
            self._participants,
            llm_client,
            HERMES_70B).compose()

        llm_speech_data_provider_factory = LlmSpeechDataProviderFactoryComposer(llm_client, HERMES_405B).compose()

        dialogue_factory = ConcreteDialogueFactory(self._messages_to_llm, self._transcription,
                                                   involve_player_in_dialogue_strategy,
                                                   speech_turn_choice_tool_response_provider_factory,
                                                   speech_turn_produce_messages_to_prompt_llm_command_factory,
                                                   llm_speech_data_provider_factory,
                                                   self._message_data_producer_for_speech_turn_strategy)

        OrchestrateDialogueProductionCommandComposer(self._playthrough_name, self._participants, llm_client,
                                                     HERMES_405B, self._dialogue_observer,
                                                     involve_player_in_dialogue_strategy,
                                                     dialogue_factory).compose().execute()
