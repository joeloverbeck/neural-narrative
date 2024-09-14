from src.abstracts.command import Command
from src.enums import PlaceType
from src.maps.abstracts.abstract_factories import RandomPlaceTemplateBasedOnCategoriesFactory
from src.maps.commands.create_random_place_type_map_entry_for_playthrough_command import \
    CreateRandomPlaceTypeMapEntryForPlaythroughCommand
from src.maps.map_manager import MapManager


class CreateInitialMapCommand(Command):
    def __init__(self, playthrough_name: str, world_template: str,
                 random_place_template_based_on_categories_factory: RandomPlaceTemplateBasedOnCategoriesFactory,
                 map_manager: MapManager = None):
        if not playthrough_name:
            raise ValueError("'playthrough_name' can't be empty.")
        if not world_template:
            raise ValueError("'world_template' can't be empty.")
        if not random_place_template_based_on_categories_factory:
            raise ValueError("'random_place_template_based_on_categories_factory' can't be empty.")

        self._playthrough_name = playthrough_name
        self._world_template = world_template
        self._random_place_template_based_on_categories_factory = random_place_template_based_on_categories_factory
        self._map_manager = map_manager or MapManager(playthrough_name)

    def execute(self) -> None:
        # Let's start with a region.
        CreateRandomPlaceTypeMapEntryForPlaythroughCommand(self._playthrough_name, None, self._world_template,
                                                           PlaceType.REGION, PlaceType.WORLD,
                                                           self._random_place_template_based_on_categories_factory).execute()

        # Retrieve the newly created region entry.
        latest_identifier, region_template = self._map_manager.get_identifier_and_place_template_of_latest_map_entry()

        # Let's follow with an area
        CreateRandomPlaceTypeMapEntryForPlaythroughCommand(self._playthrough_name, latest_identifier, region_template,
                                                           PlaceType.AREA,
                                                           PlaceType.REGION,
                                                           self._random_place_template_based_on_categories_factory).execute()

        # Retrieve the newly created area entry.
        latest_identifier, area_template = self._map_manager.get_identifier_and_place_template_of_latest_map_entry()

        CreateRandomPlaceTypeMapEntryForPlaythroughCommand(self._playthrough_name, latest_identifier, area_template,
                                                           PlaceType.LOCATION,
                                                           PlaceType.AREA,
                                                           self._random_place_template_based_on_categories_factory).execute()
