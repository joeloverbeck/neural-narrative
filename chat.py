import logging
import logging.config

import colorama

from src.dialogues.commands.launch_dialogue_command import LaunchDialogueCommand
from src.dialogues.factories.console_player_input_factory import ConsolePlayerInputFactory
from src.dialogues.observers.console_dialogue_observer import ConsoleDialogueObserver
# Import from local modules
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.playthrough_manager import PlaythroughManager


def main():
    colorama.init()

    logging.config.dictConfig(FilesystemManager().get_logging_config_file())

    interface_manager = ConsoleInterfaceManager()

    playthrough_name = interface_manager.prompt_for_input("Enter your playthrough name: ")

    player_identifier = PlaythroughManager(playthrough_name).get_player_identifier()

    # Prompt for character(s) the user wishes to speak to
    participants = interface_manager.prompt_for_multiple_identifiers(
        "Enter the identifiers of the characters you wish to speak to (separated by spaces or commas): ")

    if player_identifier:
        participants.insert(0, player_identifier)

    dialogue_observer = ConsoleDialogueObserver()

    player_input_factory = ConsolePlayerInputFactory()

    LaunchDialogueCommand(playthrough_name, player_identifier, participants, dialogue_observer,
                          player_input_factory).execute()


if __name__ == "__main__":
    main()
