from typing import List

from src.abstracts.command import Command
from src.abstracts.observer import Observer
from src.constants import HERMES_70B, HERMES_405B
from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
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
from src.dialogues.strategies.concrete_involve_player_in_dialogue_strategy import \
    ConcreteInvolvePlayerInDialogueStrategy
from src.prompting.factories.openrouter_llm_client_factory import OpenRouterLlmClientFactory


class LaunchDialogueCommand(Command):
    def __init__(self, playthrough_name: str, player_identifier: str, participants: List[str],
                 dialogue_observer: Observer,
                 player_input_factory: PlayerInputFactory):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not len(participants) >= 2:
            raise ValueError(f"Insufficient number of participants to launch dialogue: {len(participants)}.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._dialogue_observer = dialogue_observer
        self._player_input_factory = player_input_factory

    def execute(self) -> None:

        llm_client = OpenRouterLlmClientFactory().create_llm_client()

        speech_turn_choice_tool_response_provider_factory = SpeechTurnChoiceToolResponseFactoryComposer(
            self._playthrough_name,
            self._player_identifier,
            self._participants,
            llm_client,
            HERMES_70B).compose()

        llm_speech_data_provider_factory = LlmSpeechDataProviderFactoryComposer(llm_client, HERMES_405B).compose()

        introduce_player_input_into_dialogue_command_factory = IntroducePlayerInputIntoDialogueCommandFactory(
            self._playthrough_name, self._player_identifier)

        involve_player_in_dialogue_strategy = ConcreteInvolvePlayerInDialogueStrategy(self._player_identifier,
                                                                                      self._player_input_factory,
                                                                                      introduce_player_input_into_dialogue_command_factory)

        speech_turn_produce_messages_to_prompt_llm_command_factory = SpeechTurnProduceMessagesToPromptLlmCommandFactoryComposer(
            self._playthrough_name,
            self._player_identifier,
            self._participants, speech_turn_choice_tool_response_provider_factory).compose()

        dialogue_factory = ConcreteDialogueFactory(involve_player_in_dialogue_strategy,
                                                   speech_turn_produce_messages_to_prompt_llm_command_factory,
                                                   llm_speech_data_provider_factory)

        OrchestrateDialogueProductionCommandComposer(self._playthrough_name, self._participants, llm_client,
                                                     HERMES_405B, self._dialogue_observer,
                                                     involve_player_in_dialogue_strategy,
                                                     dialogue_factory).compose().execute()
