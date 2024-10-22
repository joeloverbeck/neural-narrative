import logging
from src.base.abstracts.command import Command
from src.base.enums import TemplateType
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.random_template_type_map_entry_provider_factory import RandomTemplateTypeMapEntryProviderFactory
logger = logging.getLogger(__name__)


class CreateInitialMapCommand(Command):

    def __init__(self, story_universe_template: str,
                 random_template_type_map_entry_provider_factory:
                 RandomTemplateTypeMapEntryProviderFactory, map_manager_factory:
            MapManagerFactory):
        self._story_universe_template = story_universe_template
        self._random_template_type_map_entry_provider_factory = (
            random_template_type_map_entry_provider_factory)
        self._map_manager_factory = map_manager_factory

    def _create_world(self) -> None:
        result = (self._random_template_type_map_entry_provider_factory.
                  create_provider(None, self._story_universe_template,
                                  TemplateType.STORY_UNIVERSE, TemplateType.WORLD).
                  create_random_place_type_map_entry())
        if result.get_result_type(
        ) == RandomTemplateTypeMapEntryCreationResultType.FAILURE:
            raise ValueError(
                f'Was unable to create a map entry for a world: {result.get_error()}'
            )

    def _create_region(self) -> None:
        latest_identifier, world_template = (self._map_manager_factory.
                                             create_map_manager().
                                             get_identifier_and_place_template_of_latest_map_entry())
        result = (self._random_template_type_map_entry_provider_factory.
                  create_provider(latest_identifier, world_template, TemplateType
                                  .WORLD, TemplateType.REGION).create_random_place_type_map_entry())
        if result.get_result_type(
        ) == RandomTemplateTypeMapEntryCreationResultType.FAILURE:
            raise ValueError(
                f'Was unable to create a map entry for a region: {result.get_error()}'
            )

    def _create_area(self) -> None:
        latest_identifier, region_template = (self._map_manager_factory.
                                              create_map_manager().
                                              get_identifier_and_place_template_of_latest_map_entry())
        result = (self._random_template_type_map_entry_provider_factory.
                  create_provider(latest_identifier, region_template,
                                  TemplateType.REGION, TemplateType.AREA).
                  create_random_place_type_map_entry())
        if result.get_result_type(
        ) == RandomTemplateTypeMapEntryCreationResultType.FAILURE:
            raise ValueError(
                f'Was unable to create a map entry for an area: {result.get_error()}'
            )

    def execute(self) -> None:
        self._create_world()
        self._create_region()
        self._create_area()
