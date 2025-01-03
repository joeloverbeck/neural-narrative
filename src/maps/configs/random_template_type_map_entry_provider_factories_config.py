from dataclasses import dataclass

from src.maps.abstracts.abstract_factories import (
    RandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.factories.create_map_entry_for_playthrough_command_provider_factory import (
    CreateMapEntryForPlaythroughCommandProviderFactory,
)
from src.maps.factories.filter_out_used_templates_algorithm_factory import (
    FilterOutUsedTemplatesAlgorithmFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory


@dataclass
class RandomTemplateTypeMapEntryProviderFactoriesConfig:
    random_place_template_based_on_categories_factory: (
        RandomPlaceTemplateBasedOnCategoriesFactory
    )
    create_map_entry_for_playthrough_command_provider_factory: (
        CreateMapEntryForPlaythroughCommandProviderFactory
    )
    place_manager_factory: PlaceManagerFactory
    filter_out_used_templates_algorithm_factory: FilterOutUsedTemplatesAlgorithmFactory
