import logging
import logging.config

import colorama

from src.base.playthrough_manager import PlaythroughManager
from src.dialogues.commands.setup_dialogue_command import SetupDialogueCommand
from src.dialogues.factories.console_player_input_factory import (
    ConsolePlayerInputFactory,
)
from src.dialogues.factories.handle_possible_existence_of_ongoing_conversation_command_factory import (
    HandlePossibleExistenceOfOngoingConversationCommandFactory,
)
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import (
    LoadDataFromOngoingDialogueCommandFactory,
)
from src.dialogues.observers.console_dialogue_observer import ConsoleDialogueObserver
from src.dialogues.participants import Participants
from src.dialogues.strategies.console_choose_participants_strategy import (
    ConsoleChooseParticipantsStrategy,
)
from src.dialogues.strategies.console_message_data_producer_for_introduce_player_input_into_dialogue_strategy import (
    ConsoleMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)
from src.dialogues.strategies.console_message_data_producer_for_speech_turn_strategy import (
    ConsoleMessageDataProducerForSpeechTurnStrategy,
)

# Import from local modules
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.console_interface_manager import ConsoleInterfaceManager


def main():
    colorama.init()

    filesystem_manager = FilesystemManager()

    logging.config.dictConfig(filesystem_manager.get_logging_config_file())

    interface_manager = ConsoleInterfaceManager()

    playthrough_name = interface_manager.prompt_for_input(
        "Enter your playthrough name: "
    )

    player_identifier = PlaythroughManager(playthrough_name).get_player_identifier()

    dialogue_observer = ConsoleDialogueObserver()

    player_input_factory = ConsolePlayerInputFactory()

    participants = Participants()

    load_data_from_ongoing_dialogue_command_factory = (
        LoadDataFromOngoingDialogueCommandFactory(playthrough_name, participants)
    )

    handle_possible_existence_of_ongoing_conversation_command_factory = (
        HandlePossibleExistenceOfOngoingConversationCommandFactory(
            playthrough_name,
            player_identifier,
            participants,
            load_data_from_ongoing_dialogue_command_factory,
            ConsoleChooseParticipantsStrategy(),
        )
    )

    purpose = input("Enter the purpose of the dialogue (can be empty): ")

    SetupDialogueCommand(
        playthrough_name,
        player_identifier,
        participants,
        purpose,
        dialogue_observer,
        player_input_factory,
        handle_possible_existence_of_ongoing_conversation_command_factory,
        ConsoleMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(),
        ConsoleMessageDataProducerForSpeechTurnStrategy(),
    ).execute()


if __name__ == "__main__":
    main()
