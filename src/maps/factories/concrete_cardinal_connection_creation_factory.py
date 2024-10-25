from typing import Optional

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.maps.abstracts.abstract_factories import CardinalConnectionCreationFactory
from src.maps.abstracts.factory_products import (
    CardinalConnectionCreationProduct,
    RandomTemplateTypeMapEntryCreationResult,
)
from src.maps.configs.cardinal_connection_creation_factory_config import (
    CardinalConnectionCreationFactoryConfig,
)
from src.maps.configs.cardinal_connection_creation_factory_factories_config import (
    CardinalConnectionCreationFactoryFactoriesConfig,
)
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType
from src.maps.products.concrete_cardinal_connection_creation_product import (
    ConcreteCardinalConnectionCreationProduct,
)


class ConcreteCardinalConnectionCreationFactory(CardinalConnectionCreationFactory):

    def __init__(
        self,
        config: CardinalConnectionCreationFactoryConfig,
        factories_config: CardinalConnectionCreationFactoryFactoriesConfig,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        self._config = config
        self._factories_config = factories_config
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._config.playthrough_name
        )

    def _get_random_area(self) -> RandomTemplateTypeMapEntryCreationResult:
        father_template = (
            self._factories_config.map_manager_factory.create_map_manager().get_father_template()
        )

        father_identifier = self._factories_config.hierarchy_manager_factory.create_hierarchy_manager().get_father_identifier(
            self._playthrough_manager.get_current_place_identifier()
        )

        return self._factories_config.random_template_type_map_entry_provider_factory.create_provider(
            father_identifier, father_template, TemplateType.REGION, TemplateType.AREA
        ).create_map_entry()

    def _create_cardinal_connection(self) -> None:
        new_id, _ = (
            self._factories_config.map_manager_factory.create_map_manager().get_identifier_and_place_template_of_latest_map_entry()
        )
        self._factories_config.navigation_manager_factory.create_navigation_manager().create_cardinal_connection(
            self._config.cardinal_direction,
            self._playthrough_manager.get_current_place_identifier(),
            new_id,
        )
        opposite_cardinal_direction = self._factories_config.navigation_manager_factory.create_navigation_manager().get_opposite_cardinal_direction(
            self._config.cardinal_direction
        )
        self._factories_config.navigation_manager_factory.create_navigation_manager().create_cardinal_connection(
            opposite_cardinal_direction,
            new_id,
            self._playthrough_manager.get_current_place_identifier(),
        )

    def create_cardinal_connection(self) -> CardinalConnectionCreationProduct:
        result = self._get_random_area()

        if (
            result.get_result_type()
            == RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
        ):
            return ConcreteCardinalConnectionCreationProduct(
                was_successful=False, error="No remaining areas to add to map."
            )
        if (
            result.get_result_type()
            == RandomTemplateTypeMapEntryCreationResultType.FAILURE
        ):
            return ConcreteCardinalConnectionCreationProduct(
                was_successful=False,
                error=f"Couldn't add an area {self._config.cardinal_direction.value}: {result.get_error()}",
            )
        self._create_cardinal_connection()
        return ConcreteCardinalConnectionCreationProduct(was_successful=True)
