from src.abstracts.command import Command
from src.enums import PlaceType
from src.maps.abstracts.abstract_factories import (
    RandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.enums import RandomPlaceTypeMapEntryCreationResultType
from src.maps.factories.concrete_random_place_type_map_entry_creation_factory import (
    ConcreteRandomPlaceTypeMapEntryCreationFactory,
)
from src.maps.factories.create_map_entry_for_playthrough_command_factory import (
    CreateMapEntryForPlaythroughCommandFactory,
)
from src.maps.map_manager import MapManager


class CreateInitialMapCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        world_template: str,
        random_place_template_based_on_categories_factory: RandomPlaceTemplateBasedOnCategoriesFactory,
        map_manager: MapManager = None,
    ):
        if not playthrough_name:
            raise ValueError("'playthrough_name' can't be empty.")
        if not world_template:
            raise ValueError("'world_template' can't be empty.")
        if not random_place_template_based_on_categories_factory:
            raise ValueError(
                "'random_place_template_based_on_categories_factory' can't be empty."
            )

        self._playthrough_name = playthrough_name
        self._world_template = world_template
        self._random_place_template_based_on_categories_factory = (
            random_place_template_based_on_categories_factory
        )
        self._map_manager = map_manager or MapManager(playthrough_name)

    def execute(self) -> None:
        # Let's start with a region.
        result = ConcreteRandomPlaceTypeMapEntryCreationFactory(
            self._playthrough_name,
            self._world_template,
            PlaceType.REGION,
            PlaceType.WORLD,
            self._random_place_template_based_on_categories_factory,
            CreateMapEntryForPlaythroughCommandFactory(
                self._playthrough_name, None, PlaceType.REGION
            ),
        ).create_random_place_type_map_entry()

        if (
            result.get_result_type()
            == RandomPlaceTypeMapEntryCreationResultType.FAILURE
        ):
            raise ValueError(
                f"Was unable to create a map entry for a region: {result.get_error()}"
            )

        # Retrieve the newly created region entry.
        latest_identifier, region_template = (
            self._map_manager.get_identifier_and_place_template_of_latest_map_entry()
        )

        # Let's follow with an area
        result = ConcreteRandomPlaceTypeMapEntryCreationFactory(
            self._playthrough_name,
            region_template,
            PlaceType.AREA,
            PlaceType.REGION,
            self._random_place_template_based_on_categories_factory,
            CreateMapEntryForPlaythroughCommandFactory(
                self._playthrough_name, latest_identifier, PlaceType.AREA
            ),
        ).create_random_place_type_map_entry()

        if (
            result.get_result_type()
            == RandomPlaceTypeMapEntryCreationResultType.FAILURE
        ):
            raise ValueError(
                f"Was unable to create a map entry for an area: {result.get_error()}"
            )

        # Retrieve the newly created area entry.
        latest_identifier, area_template = (
            self._map_manager.get_identifier_and_place_template_of_latest_map_entry()
        )

        result = ConcreteRandomPlaceTypeMapEntryCreationFactory(
            self._playthrough_name,
            area_template,
            PlaceType.LOCATION,
            PlaceType.AREA,
            self._random_place_template_based_on_categories_factory,
            CreateMapEntryForPlaythroughCommandFactory(
                self._playthrough_name, latest_identifier, PlaceType.LOCATION
            ),
        ).create_random_place_type_map_entry()

        if (
            result.get_result_type()
            == RandomPlaceTypeMapEntryCreationResultType.FAILURE
        ):
            raise ValueError(
                f"Was unable to create a map entry for a location: {result.get_error()}"
            )
