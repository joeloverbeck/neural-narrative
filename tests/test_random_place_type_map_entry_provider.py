from typing import cast
from unittest.mock import Mock, patch
from src.base.enums import TemplateType
from src.maps.abstracts.abstract_factories import (
    RandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.abstracts.factory_products import PlaceTemplateProduct
from src.maps.configs.random_template_type_map_entry_provider_config import (
    RandomTemplateTypeMapEntryProviderConfig,
)
from src.maps.configs.random_template_type_map_entry_provider_factories_config import (
    RandomTemplateTypeMapEntryProviderFactoriesConfig,
)
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType
from src.maps.providers.concrete_random_place_type_map_entry_provider import (
    ConcreteRandomTemplateTypeMapEntryProvider,
)


def test_no_available_templates():
    config = RandomTemplateTypeMapEntryProviderConfig(
        father_identifier="parent1",
        father_template="template1",
        place_type=TemplateType.WORLD,
        father_place_type=TemplateType.STORY_UNIVERSE,
    )
    factories_config = RandomTemplateTypeMapEntryProviderFactoriesConfig(
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory, Mock()
        ),
        create_map_entry_for_playthrough_command_provider_factory=Mock(),
        place_manager_factory=Mock(),
    )
    filesystem_manager = Mock()
    templates_repository = Mock()
    templates_repository.load_template.return_value = {}
    provider = ConcreteRandomTemplateTypeMapEntryProvider(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
        templates_repository=templates_repository,
    )
    result = provider.create_random_place_type_map_entry()
    assert (
        result.get_result_type()
        == RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
    )
    assert result.get_error() is None


def test_create_template_product_invalid():
    config = RandomTemplateTypeMapEntryProviderConfig(
        father_identifier="parent1",
        father_template="template1",
        place_type=TemplateType.WORLD,
        father_place_type=TemplateType.STORY_UNIVERSE,
    )
    factories_config = RandomTemplateTypeMapEntryProviderFactoriesConfig(
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory, Mock()
        ),
        create_map_entry_for_playthrough_command_provider_factory=Mock(),
        place_manager_factory=Mock(),
    )
    filesystem_manager = Mock()
    templates_repository = Mock()
    templates_repository.load_template.return_value = {"template_key": "template_value"}
    provider = ConcreteRandomTemplateTypeMapEntryProvider(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
        templates_repository=templates_repository,
    )
    mock_template_product = Mock(spec=PlaceTemplateProduct)
    mock_template_product.is_valid.return_value = False
    mock_template_product.get_error.return_value = "Invalid template product error"
    with patch.object(
        provider, "_create_template_product", return_value=mock_template_product
    ):
        result = provider.create_random_place_type_map_entry()
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert (
        result.get_error()
        == f"Wasn't able to produce a {config.place_type} template: Invalid template product error"
    )


def test_exception_during_command_execution():
    config = RandomTemplateTypeMapEntryProviderConfig(
        father_identifier="parent1",
        father_template="template1",
        place_type=TemplateType.WORLD,
        father_place_type=TemplateType.STORY_UNIVERSE,
    )
    place_manager_factory = Mock()
    place_manager = Mock()
    place_manager.get_place_categories.return_value = [Mock(value="category1")]
    place_manager_factory.create_place_manager.return_value = place_manager
    random_place_template_based_on_categories_factory = Mock()
    template_product = Mock(spec=PlaceTemplateProduct)
    template_product.is_valid.return_value = True
    template_product.get.return_value = "valid_template"
    (
        random_place_template_based_on_categories_factory.create_random_place_template_based_on_categories.return_value
    ) = template_product
    create_map_entry_provider_factory = Mock()
    create_provider = Mock()
    create_command = Mock()
    create_command.execute.side_effect = Exception("Command execution error")
    create_provider.create_command.return_value = create_command
    create_map_entry_provider_factory.create_provider.return_value = create_provider
    factories_config = RandomTemplateTypeMapEntryProviderFactoriesConfig(
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory,
            random_place_template_based_on_categories_factory,
        ),
        create_map_entry_for_playthrough_command_provider_factory=create_map_entry_provider_factory,
        place_manager_factory=place_manager_factory,
    )
    filesystem_manager = Mock()
    templates_repository = Mock()
    templates_repository.load_template.return_value = {"template_key": "template_value"}
    provider = ConcreteRandomTemplateTypeMapEntryProvider(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
        templates_repository=templates_repository,
    )
    result = provider.create_random_place_type_map_entry()
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert "Command execution error" in result.get_error()


def test_exception_during_load_templates():
    config = RandomTemplateTypeMapEntryProviderConfig(
        father_identifier="parent1",
        father_template="template1",
        place_type=TemplateType.WORLD,
        father_place_type=TemplateType.STORY_UNIVERSE,
    )
    factories_config = RandomTemplateTypeMapEntryProviderFactoriesConfig(
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory, Mock()
        ),
        create_map_entry_for_playthrough_command_provider_factory=Mock(),
        place_manager_factory=Mock(),
    )
    filesystem_manager = Mock()
    templates_repository = Mock()
    templates_repository.load_template.side_effect = Exception("Load templates error")
    provider = ConcreteRandomTemplateTypeMapEntryProvider(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
        templates_repository=templates_repository,
    )
    result = provider.create_random_place_type_map_entry()
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert "Load templates error" in result.get_error()


def test_template_product_error_is_none():
    config = RandomTemplateTypeMapEntryProviderConfig(
        father_identifier="parent1",
        father_template="template1",
        place_type=TemplateType.WORLD,
        father_place_type=TemplateType.STORY_UNIVERSE,
    )
    factories_config = RandomTemplateTypeMapEntryProviderFactoriesConfig(
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory, Mock()
        ),
        create_map_entry_for_playthrough_command_provider_factory=Mock(),
        place_manager_factory=Mock(),
    )
    filesystem_manager = Mock()
    templates_repository = Mock()
    templates_repository.load_template.return_value = {"template_key": "template_value"}
    provider = ConcreteRandomTemplateTypeMapEntryProvider(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
        templates_repository=templates_repository,
    )
    mock_template_product = Mock(spec=PlaceTemplateProduct)
    mock_template_product.is_valid.return_value = False
    mock_template_product.get_error.return_value = None
    with patch.object(
        provider, "_create_template_product", return_value=mock_template_product
    ):
        result = provider.create_random_place_type_map_entry()
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert (
        result.get_error()
        == f"Wasn't able to produce a {config.place_type} template: None"
    )
