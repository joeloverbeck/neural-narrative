import os

from src.abstracts.command import Command
from src.abstracts.observer import Observer
from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.strategies import MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy, \
    MessageDataProducerForSpeechTurnStrategy, ChooseParticipantsStrategy
from src.dialogues.commands.launch_dialogue_command import LaunchDialogueCommand
from src.dialogues.dialogue_manager import DialogueManager
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.abstracts.interface_manager import InterfaceManager
from src.interfaces.console_interface_manager import ConsoleInterfaceManager


# Import from local modules


class SetupDialogueCommand(Command):
    def __init__(self, playthrough_name: str, player_identifier: str, participants: Participants,
                 dialogue_observer: Observer,
                 player_input_factory: PlayerInputFactory,
                 message_data_producer_for_introduce_player_input_into_dialogue_strategy: MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
                 message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
                 choose_participants_strategy: ChooseParticipantsStrategy,
                 filesystem_manager: FilesystemManager = None, interface_manager: InterfaceManager = None,
                 dialogue_manager: DialogueManager = None):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")
        if not player_identifier:
            raise ValueError("player_identifier must not be empty.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._dialogue_observer = dialogue_observer
        self._player_input_factory = player_input_factory
        self._message_data_producer_for_introduce_player_input_into_dialogue_strategy = message_data_producer_for_introduce_player_input_into_dialogue_strategy
        self._message_data_producer_for_speech_turn_strategy = message_data_producer_for_speech_turn_strategy
        self._choose_participants_strategy = choose_participants_strategy

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._interface_manager = interface_manager or ConsoleInterfaceManager()
        self._dialogue_manager = dialogue_manager or DialogueManager(self._playthrough_name)

    def execute(self) -> None:
        messages_to_llm = MessagesToLlm()
        transcription = Transcription()

        # It could be that there's an ongoing dialogue active.
        if os.path.exists(self._filesystem_manager.get_file_path_to_ongoing_dialogue(self._playthrough_name)):
            # Must load the data from the ongoing dialogue.
            ongoing_dialogue_file = self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_ongoing_dialogue(self._playthrough_name))

            # Add the existing participants from the ongoing dialogue to the participants class.
            for identifier, participant in ongoing_dialogue_file["participants"].items():
                self._participants.add_participant(identifier, participant["name"],
                                                   participant["description"], participant["personality"],
                                                   participant["equipment"])

            for message in ongoing_dialogue_file["messages_to_llm"]:
                messages_to_llm.add_message(message["role"], message["content"])

            for speech_turn in ongoing_dialogue_file["transcription"]:
                transcription.add_speech_line(speech_turn)

        else:
            # Prompt for character(s) the user wishes to speak to
            chosen_participants = self._choose_participants_strategy.choose_participants()

            # gather participant data
            self._dialogue_manager.gather_participants_data(self._player_identifier, chosen_participants,
                                                            self._participants)

        LaunchDialogueCommand(self._playthrough_name, self._player_identifier, self._participants, messages_to_llm,
                              transcription,
                              self._dialogue_observer,
                              self._player_input_factory,
                              self._message_data_producer_for_introduce_player_input_into_dialogue_strategy,
                              self._message_data_producer_for_speech_turn_strategy).execute()
