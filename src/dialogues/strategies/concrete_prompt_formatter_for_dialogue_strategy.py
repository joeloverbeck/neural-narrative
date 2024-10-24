from typing import Optional

from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
from src.dialogues.abstracts.strategies import PromptFormatterForDialogueStrategy
from src.dialogues.participants import Participants
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.time.time_manager import TimeManager


class ConcretePromptFormatterForDialogueStrategy(PromptFormatterForDialogueStrategy):

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        purpose: Optional[str],
        name: str,
        character_information_factory: CharacterInformationProvider,
        prompt_file: str,
        places_descriptions_factory: PlacesDescriptionsProvider,
        filesystem_manager: FilesystemManager = None,
    ):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose
        self._name = name
        self._character_information_factory = character_information_factory
        self._prompt_file = prompt_file
        self._places_descriptions_factory = places_descriptions_factory
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _format_participant_details(self) -> str:
        return "\n".join(
            [
                f"{participant['name']}: {participant['description']}. Equipment: {participant['equipment']}"
                for _, participant in self._participants.get().items()
                if participant["name"] != self._name
            ]
        )

    def _format_dialogue_purpose(self) -> str:
        if self._purpose:
            return f"The purpose of this dialogue is: {self._purpose}"
        return ""

    def do_algorithm(self) -> str:
        time_manager = TimeManager(self._playthrough_name)
        participant_details = self._format_participant_details()
        dialogue_purpose = self._format_dialogue_purpose()
        return self._filesystem_manager.read_file(self._prompt_file).format(
            places_descriptions=self._places_descriptions_factory.get_information(),
            hour=time_manager.get_hour(),
            time_group=time_manager.get_time_of_the_day(),
            name=self._name,
            participant_details=participant_details,
            character_information=self._character_information_factory.get_information(),
            dialogue_purpose=dialogue_purpose,
        )
