import logging
from typing import Dict, Optional

from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import (
    RandomTemplateTypeMapEntryProvider,
)
from src.maps.abstracts.factory_products import (
    RandomTemplateTypeMapEntryCreationResult,
    PlaceTemplateProduct,
)
from src.maps.configs.random_template_type_map_entry_provider_config import (
    RandomTemplateTypeMapEntryProviderConfig,
)
from src.maps.configs.random_template_type_map_entry_provider_factories_config import (
    RandomTemplateTypeMapEntryProviderFactoriesConfig,
)
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType
from src.maps.products.concrete_random_place_type_map_entry_creation_result import (
    ConcreteRandomTemplateTypeMapEntryCreationResult,
)
from src.maps.templates_repository import TemplatesRepository

logger = logging.getLogger(__name__)


class ConcreteRandomTemplateTypeMapEntryProvider(RandomTemplateTypeMapEntryProvider):
    def __init__(
        self,
            config: RandomTemplateTypeMapEntryProviderConfig,
            factories_config: RandomTemplateTypeMapEntryProviderFactoriesConfig,
            filesystem_manager: Optional[FilesystemManager] = None,
            templates_repository: Optional[TemplatesRepository] = None,
    ):
        self._config = config
        self._factories_config = factories_config

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._templates_repository = templates_repository or TemplatesRepository(
            self._filesystem_manager
        )

    def _create_template_product(
            self, available_templates: Dict
    ) -> PlaceTemplateProduct:
        categories = self._factories_config.place_manager_factory.create_place_manager().get_place_categories(
            self._config.father_template, self._config.father_place_type
        )
        return self._factories_config.random_place_template_based_on_categories_factory.create_random_place_template_based_on_categories(
            available_templates, categories
        )

    def create_random_place_type_map_entry(
        self,
    ) -> RandomTemplateTypeMapEntryCreationResult:
        try:
            available_templates = self._templates_repository.load_template(
                self._config.place_type
            )

            if not available_templates:
                return ConcreteRandomTemplateTypeMapEntryCreationResult(
                    RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
                )

            template_product = self._create_template_product(available_templates)

            if not template_product.is_valid():
                return ConcreteRandomTemplateTypeMapEntryCreationResult(
                    RandomTemplateTypeMapEntryCreationResultType.FAILURE,
                    f"Wasn't able to produce a {self._config.place_type.value} template: {template_product.get_error()}",
                )

            self._factories_config.create_map_entry_for_playthrough_command_provider_factory.create_provider(
                self._config.father_identifier, self._config.place_type
            ).create_command(
                template_product.get()
            ).execute()

            return ConcreteRandomTemplateTypeMapEntryCreationResult(
                RandomTemplateTypeMapEntryCreationResultType.SUCCESS
            )

        except Exception as e:
            return ConcreteRandomTemplateTypeMapEntryCreationResult(
                RandomTemplateTypeMapEntryCreationResultType.FAILURE, str(e)
            )
