from src.abstracts.command import Command
from src.characters.factories.generate_random_characters_command_factory import (
    GenerateRandomCharactersCommandFactory,
)
from src.constants import TIME_ADVANCED_DUE_TO_EXITING_LOCATION
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.time.time_manager import TimeManager


class VisitPlaceCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        place_identifier: str,
        generate_random_characters_command_factory: GenerateRandomCharactersCommandFactory,
        playthrough_manager: PlaythroughManager = None,
        map_manager: MapManager = None,
        time_manager: TimeManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._place_identifier = place_identifier
        self._generate_random_characters_command_factory = (
            generate_random_characters_command_factory
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._time_manager = time_manager or TimeManager(self._playthrough_name)

    def execute(self) -> None:
        self._playthrough_manager.update_current_place(self._place_identifier)

        # Mechanics related to whether or not the location has been visit should go here.
        # Now delegate creating a few characters at the location.
        if not self._map_manager.is_visited(self._place_identifier):
            self._generate_random_characters_command_factory.create_generate_random_characters_command(
                self._map_manager.fill_places_parameter(self._place_identifier)
            ).execute()

            # Now set the place as visited.
            self._map_manager.set_as_visited(self._place_identifier)

        # Advance time.
        self._time_manager.advance_time(TIME_ADVANCED_DUE_TO_EXITING_LOCATION)
