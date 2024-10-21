from dataclasses import dataclass

from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.navigation_manager_factory import NavigationManagerFactory
from src.maps.factories.random_template_type_map_entry_provider_factory import (
    RandomTemplateTypeMapEntryProviderFactory,
)


@dataclass
class CardinalConnectionCreationFactoryFactoriesConfig:
    random_template_type_map_entry_provider_factory: (
        RandomTemplateTypeMapEntryProviderFactory
    )
    hierarchy_manager_factory: HierarchyManagerFactory
    map_manager_factory: MapManagerFactory
    navigation_manager_factory: NavigationManagerFactory
