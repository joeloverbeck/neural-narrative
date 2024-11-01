import logging
from typing import Dict, Optional

from src.base.products.text_product import TextProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import RandomTemplateTypeMapEntryProvider
from src.maps.abstracts.factory_products import (
    RandomTemplateTypeMapEntryCreationResult,
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

logger = logging.getLogger(__name__)


class ConcreteRandomPlaceTypeMapEntryProvider(RandomTemplateTypeMapEntryProvider):

    def __init__(
        self,
        config: RandomTemplateTypeMapEntryProviderConfig,
        factories_config: RandomTemplateTypeMapEntryProviderFactoriesConfig,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._config = config
        self._factories_config = factories_config

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _get_available_templates(self) -> Dict:
        """Retrieve available templates by filtering out used ones."""
        filter_factory = (
            self._factories_config.filter_out_used_templates_algorithm_factory
        )
        filter_algorithm = filter_factory.create_factory(self._config.place_type)
        return filter_algorithm.do_algorithm()

    def _create_template_product(self, available_templates: Dict) -> TextProduct:
        categories = self._factories_config.place_manager_factory.create_place_manager().get_place_categories(
            self._config.father_template, self._config.father_place_type
        )
        return self._factories_config.random_place_template_based_on_categories_factory.create_place(
            available_templates, categories
        )

    def _execute_create_map_entry_command(self, template: str):
        """Execute the command to create a map entry for the playthrough."""
        command_provider_factory = (
            self._factories_config.create_map_entry_for_playthrough_command_provider_factory
        )
        command_provider = command_provider_factory.create_provider(
            self._config.father_identifier, self._config.place_type
        )
        command = command_provider.create_command(template)
        command.execute()

    def create_map_entry(
        self,
    ) -> RandomTemplateTypeMapEntryCreationResult:
        try:
            available_templates = self._get_available_templates()
            if not available_templates:
                return ConcreteRandomTemplateTypeMapEntryCreationResult(
                    RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
                )

            template_product = self._create_template_product(available_templates)

            if not template_product.is_valid():
                error_message = (
                    f"Failed to produce a {self._config.place_type} template: "
                    f"{template_product.get_error()}"
                )
                return ConcreteRandomTemplateTypeMapEntryCreationResult(
                    RandomTemplateTypeMapEntryCreationResultType.FAILURE, error_message
                )

            self._execute_create_map_entry_command(template_product.get())

            return ConcreteRandomTemplateTypeMapEntryCreationResult(
                RandomTemplateTypeMapEntryCreationResultType.SUCCESS
            )
        except Exception as e:
            logger.exception("An error occurred while creating map entry.")
            return ConcreteRandomTemplateTypeMapEntryCreationResult(
                RandomTemplateTypeMapEntryCreationResultType.FAILURE, str(e)
            )
