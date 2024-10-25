from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.base.enums import IdentifierType
from src.base.factories.store_last_identifier_command_factory import (
    StoreLastIdentifierCommandFactory,
)
from src.maps.composers.place_selection_manager_composer import (
    PlaceSelectionManagerComposer,
)
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.factories.create_map_entry_for_playthrough_command_provider_factory import (
    CreateMapEntryForPlaythroughCommandProviderFactory,
)
from src.maps.factories.filter_out_used_templates_algorithm_factory import (
    FilterOutUsedTemplatesAlgorithmFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.random_template_type_map_entry_provider_factory import (
    RandomTemplateTypeMapEntryProviderFactory,
)


class RandomTemplateTypeMapEntryProviderFactoryComposer:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def compose_factory(self) -> RandomTemplateTypeMapEntryProviderFactory:
        place_selection_manager = PlaceSelectionManagerComposer(
            self._playthrough_name
        ).compose_manager()
        random_place_template_based_on_categories_factory = (
            ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(place_selection_manager)
        )

        store_last_identifier_command_factory = StoreLastIdentifierCommandFactory(
            self._playthrough_name
        )

        produce_and_update_next_identifier = ProduceAndUpdateNextIdentifierAlgorithm(
            self._playthrough_name,
            IdentifierType.PLACES,
            store_last_identifier_command_factory,
        )

        create_map_entry_for_playthrough_command_provider_factory = (
            CreateMapEntryForPlaythroughCommandProviderFactory(
                self._playthrough_name, produce_and_update_next_identifier
            )
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
