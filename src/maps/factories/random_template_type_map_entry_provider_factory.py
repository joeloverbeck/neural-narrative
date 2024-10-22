from typing import Optional
from src.base.enums import TemplateType
from src.maps.abstracts.abstract_factories import RandomTemplateTypeMapEntryProvider, \
    RandomPlaceTemplateBasedOnCategoriesFactory
from src.maps.configs.random_template_type_map_entry_provider_config import RandomTemplateTypeMapEntryProviderConfig
from src.maps.configs.random_template_type_map_entry_provider_factories_config import \
    RandomTemplateTypeMapEntryProviderFactoriesConfig
from src.maps.factories.create_map_entry_for_playthrough_command_provider_factory import \
    CreateMapEntryForPlaythroughCommandProviderFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.providers.concrete_random_place_type_map_entry_provider import ConcreteRandomTemplateTypeMapEntryProvider


class RandomTemplateTypeMapEntryProviderFactory:

    def __init__(self, playthrough_name: str,
                 random_place_template_based_on_categories_factory:
                 RandomPlaceTemplateBasedOnCategoriesFactory,
                 create_map_entry_for_playthrough_command_provider_factory:
                 CreateMapEntryForPlaythroughCommandProviderFactory,
                 place_manager_factory: PlaceManagerFactory):
        self._playthrough_name = playthrough_name
        self._random_place_template_based_on_categories_factory = (
            random_place_template_based_on_categories_factory)
        self._create_map_entry_for_playthrough_command_provider_factory = (
            create_map_entry_for_playthrough_command_provider_factory)
        self._place_manager_factory = place_manager_factory

    def create_provider(self, father_identifier: Optional[str],
                        father_template: str, father_place_type: TemplateType,
                        new_place_type: TemplateType) -> RandomTemplateTypeMapEntryProvider:
        return ConcreteRandomTemplateTypeMapEntryProvider(config=
                                                          RandomTemplateTypeMapEntryProviderConfig(father_identifier,
                                                                                                   father_template,
                                                                                                   new_place_type,
                                                                                                   father_place_type),
                                                          factories_config=
                                                          RandomTemplateTypeMapEntryProviderFactoriesConfig(self.
                                                                                                            _random_place_template_based_on_categories_factory,
                                                                                                            self.
                                                                                                            _create_map_entry_for_playthrough_command_provider_factory,
                                                                                                            self._place_manager_factory))
