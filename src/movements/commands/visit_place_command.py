from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_character_generation_guidelines_command import (
    GenerateCharacterGenerationGuidelinesCommand,
)
from src.characters.factories.character_generation_guidelines_factory import (
    CharacterGenerationGuidelinesFactory,
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
        character_generation_guidelines_factory: CharacterGenerationGuidelinesFactory,
        playthrough_manager: PlaythroughManager = None,
        map_manager: MapManager = None,
        time_manager: TimeManager = None,
        characters_manager: CharactersManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._place_identifier = place_identifier
        self._character_generation_guidelines_factory = (
            character_generation_guidelines_factory
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._time_manager = time_manager or TimeManager(self._playthrough_name)
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def _handle_place_is_not_visited(self):
        # If the place hasn't been visited, then generally the character generation guidelines haven't been generated.
        world_name = self._playthrough_manager.get_world_template()

        places_templates_parameter = self._map_manager.fill_places_templates_parameter(
            self._place_identifier
        )

        if not self._characters_manager.are_there_character_generation_guidelines_for_place(
            world_name,
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            places_templates_parameter.get_location_template(),
        ):
            # We need to create the character generation guidelines for this location.
            GenerateCharacterGenerationGuidelinesCommand(
                self._playthrough_name,
                self._place_identifier,
                self._character_generation_guidelines_factory,
            ).execute()

        # Now set the place as visited.
        self._map_manager.set_as_visited(self._place_identifier)

    def execute(self) -> None:
        # Careful moving the following code, about updating the current place of the playthrough,
        # because generation of characters uses whatever is the current place of the playthrough.
        self._playthrough_manager.update_current_place(self._place_identifier)

        if not self._map_manager.is_visited(self._place_identifier):
            self._handle_place_is_not_visited()

        # Advance time.
        self._time_manager.advance_time(TIME_ADVANCED_DUE_TO_EXITING_LOCATION)
