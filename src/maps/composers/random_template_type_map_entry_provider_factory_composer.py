from src.base.required_string import RequiredString
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.factories.create_map_entry_for_playthrough_command_provider_factory import (
    CreateMapEntryForPlaythroughCommandProviderFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.random_template_type_map_entry_provider_factory import (
    RandomTemplateTypeMapEntryProviderFactory,
)
from src.maps.place_selection_manager import PlaceSelectionManager
from src.maps.templates_repository import TemplatesRepository


class RandomTemplateTypeMapEntryProviderFactoryComposer:
    def __init__(
        self,
        playthrough_name: RequiredString,
    ):
        self._playthrough_name = playthrough_name

    def compose_factory(self) -> RandomTemplateTypeMapEntryProviderFactory:
        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        template_repository = TemplatesRepository()

        place_selection_manager = PlaceSelectionManager(
            place_manager_factory, template_repository
        )

        random_place_template_based_on_categories_factory = (
            ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(place_selection_manager)
        )

        create_map_entry_for_playthrough_command_provider_factory = (
            CreateMapEntryForPlaythroughCommandProviderFactory(self._playthrough_name)
        )

        return RandomTemplateTypeMapEntryProviderFactory(
            self._playthrough_name,
            random_place_template_based_on_categories_factory,
            create_map_entry_for_playthrough_command_provider_factory,
            place_manager_factory,
        )
