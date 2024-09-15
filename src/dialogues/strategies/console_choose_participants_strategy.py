from typing import List

from src.dialogues.abstracts.strategies import ChooseParticipantsStrategy
from src.interfaces.console_interface_manager import ConsoleInterfaceManager


class ConsoleChooseParticipantsStrategy(ChooseParticipantsStrategy):
    def __init__(self, interface_manager: ConsoleInterfaceManager = None):
        self._interface_manager = interface_manager or ConsoleInterfaceManager()

    def choose_participants(self) -> List[str]:
        return self._interface_manager.prompt_for_multiple_identifiers(
            "Enter the identifiers of the characters you wish to speak to (separated by spaces or commas): ")
