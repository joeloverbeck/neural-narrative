from typing import Optional

from src.maps.composers.create_map_entry_for_playthrough_command_provider_factory_composer import (
    CreateMapEntryForPlaythroughCommandProviderFactoryComposer,
)
from src.maps.composers.place_selection_manager_composer import (
    PlaceSelectionManagerComposer,
)
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.factories.filter_out_used_templates_algorithm_factory import (
    FilterOutUsedTemplatesAlgorithmFactory,
)
from src.maps.factories.filter_places_by_categories_algorithm_factory import (
    FilterPlacesByCategoriesAlgorithmFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.random_template_type_map_entry_provider_factory import (
    RandomTemplateTypeMapEntryProviderFactory,
)


class RandomTemplateTypeMapEntryProviderFactoryComposer:

    def __init__(
        self, playthrough_name: str, location_or_room_type: Optional[str] = None
    ):
        self._playthrough_name = playthrough_name
        self._location_or_room_type = location_or_room_type

    def compose_factory(self) -> RandomTemplateTypeMapEntryProviderFactory:
        place_selection_manager = PlaceSelectionManagerComposer(
            self._playthrough_name
        ).compose_manager()

        filter_places_by_categories_algorithm_factory = (
            FilterPlacesByCategoriesAlgorithmFactory(self._location_or_room_type)
        )

        random_place_template_based_on_categories_factory = (
            ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
                filter_places_by_categories_algorithm_factory, place_selection_manager
            )
        )

        create_map_entry_for_playthrough_command_provider_factory = (
            CreateMapEntryForPlaythroughCommandProviderFactoryComposer(
                self._playthrough_name
            ).create_factory()
        )

        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        filter_out_used_templates_algorithm_factory = (
            FilterOutUsedTemplatesAlgorithmFactory(place_manager_factory)
        )

        return RandomTemplateTypeMapEntryProviderFactory(
            random_place_template_based_on_categories_factory,
            create_map_entry_for_playthrough_command_provider_factory,
            filter_out_used_templates_algorithm_factory,
            place_manager_factory,
        )
