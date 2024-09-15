import logging
import logging.config

import colorama

from src.dialogues.commands.setup_dialogue_command import SetupDialogueCommand
from src.dialogues.factories.console_player_input_factory import ConsolePlayerInputFactory
from src.dialogues.observers.console_dialogue_observer import ConsoleDialogueObserver
from src.dialogues.participants import Participants
from src.dialogues.strategies.console_choose_participants_strategy import ConsoleChooseParticipantsStrategy
from src.dialogues.strategies.console_message_data_producer_for_introduce_player_input_into_dialogue_strategy import \
    ConsoleMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy
from src.dialogues.strategies.console_message_data_producer_for_speech_turn_strategy import \
    ConsoleMessageDataProducerForSpeechTurnStrategy
# Import from local modules
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.playthrough_manager import PlaythroughManager


def main():
    colorama.init()

    filesystem_manager = FilesystemManager()

    logging.config.dictConfig(filesystem_manager.get_logging_config_file())

    interface_manager = ConsoleInterfaceManager()

    playthrough_name = interface_manager.prompt_for_input("Enter your playthrough name: ")

    player_identifier = PlaythroughManager(playthrough_name).get_player_identifier()

    dialogue_observer = ConsoleDialogueObserver()

    player_input_factory = ConsolePlayerInputFactory()

    participants = Participants()

    SetupDialogueCommand(playthrough_name, player_identifier, participants, dialogue_observer, player_input_factory,
                         ConsoleMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(),
                         ConsoleMessageDataProducerForSpeechTurnStrategy(),
                         ConsoleChooseParticipantsStrategy()).execute()


if __name__ == "__main__":
    main()
