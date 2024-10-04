from typing import Dict

from src.enums import PlaceType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import (
    RandomPlaceTypeMapEntryCreationFactory,
    RandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.abstracts.factory_products import (
    RandomPlaceTypeMapEntryCreationResult,
    PlaceTemplateProduct,
)
from src.maps.enums import RandomPlaceTypeMapEntryCreationResultType
from src.maps.factories.create_map_entry_for_playthrough_command_factory import (
    CreateMapEntryForPlaythroughCommandFactory,
)
from src.maps.map_manager import MapManager
from src.maps.products.concrete_random_place_type_map_entry_creation_result import (
    ConcreteRandomPlaceTypeMapEntryCreationResult,
)


class ConcreteRandomPlaceTypeMapEntryCreationFactory(
    RandomPlaceTypeMapEntryCreationFactory
):
    def __init__(
        self,
        playthrough_name: str,
        father_template: str,
        place_type: PlaceType,
        father_place_type: PlaceType,
        random_place_template_based_on_categories_factory: RandomPlaceTemplateBasedOnCategoriesFactory,
        create_map_entry_for_playthrough_command_factory: CreateMapEntryForPlaythroughCommandFactory,
        filesystem_manager: FilesystemManager = None,
        map_manager: MapManager = None,
    ):
        if not playthrough_name:
            raise ValueError("'playthrough_name' can't be empty.")
        if not father_template:
            raise ValueError("'father_template' can't be empty.")

        self._father_template = father_template
        self._place_type = place_type
        self._father_place_type = father_place_type
        self._random_place_template_based_on_categories_factory = (
            random_place_template_based_on_categories_factory
        )
        self._create_map_entry_for_playthrough_command_factory = (
            create_map_entry_for_playthrough_command_factory
        )

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._map_manager = map_manager or MapManager(playthrough_name)

    def create_random_place_type_map_entry(
        self,
    ) -> RandomPlaceTypeMapEntryCreationResult:
        try:
            place_templates_file_path = self._get_template_file_path()
            available_templates = self._load_and_filter_templates(
                place_templates_file_path
            )

            if not available_templates:
                return ConcreteRandomPlaceTypeMapEntryCreationResult(
                    RandomPlaceTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
                )

            template_product = self._create_template_product(available_templates)

            if not template_product.is_valid():
                return ConcreteRandomPlaceTypeMapEntryCreationResult(
                    RandomPlaceTypeMapEntryCreationResultType.FAILURE,
                    f"Wasn't able to produce a {self._place_type.value} template: {template_product.get_error()}",
                )

            self._create_map_entry_for_playthrough_command_factory.create_command(
                template_product.get()
            ).execute()

            return ConcreteRandomPlaceTypeMapEntryCreationResult(
                RandomPlaceTypeMapEntryCreationResultType.SUCCESS
            )

        except Exception as e:
            return ConcreteRandomPlaceTypeMapEntryCreationResult(
                RandomPlaceTypeMapEntryCreationResultType.FAILURE, str(e)
            )

    def _get_template_file_path(self) -> str:
        place_type_to_method = {
            PlaceType.REGION: self._filesystem_manager.get_file_path_to_regions_template_file,
            PlaceType.AREA: self._filesystem_manager.get_file_path_to_areas_template_file,
            PlaceType.LOCATION: self._filesystem_manager.get_file_path_to_locations_template_file,
        }

        method = place_type_to_method.get(self._place_type)

        if not method:
            raise NotImplementedError(
                f"Creation of map entries for '{self._place_type.value}' is not supported."
            )

        return method()

    def _load_and_filter_templates(self, template_file_path: str) -> Dict:
        templates = self._filesystem_manager.load_existing_or_new_json_file(
            template_file_path
        )
        used_templates = self._map_manager.get_place_templates_of_type(self._place_type)
        return {
            name: data for name, data in templates.items() if name not in used_templates
        }

    def _create_template_product(
        self, available_templates: Dict
    ) -> PlaceTemplateProduct:
        categories = self._map_manager.get_place_categories(
            self._father_template, self._father_place_type
        )
        return self._random_place_template_based_on_categories_factory.create_random_place_template_based_on_categories(
            available_templates, categories
        )
