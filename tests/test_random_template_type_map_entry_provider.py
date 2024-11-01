from unittest.mock import Mock, patch

import pytest

from src.base.products.text_product import TextProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType
from src.maps.providers.concrete_random_place_type_map_entry_provider import (
    ConcreteRandomPlaceTypeMapEntryProvider,
)


# Fixtures for configuration and factories


@pytest.fixture
def provider_config():
    return Mock(
        father_identifier="father_id",
        father_template="father_template",
        place_type="PLACE_TYPE",
        father_place_type="FATHER_PLACE_TYPE",
    )


@pytest.fixture
def factories_config():
    # Mock all factory dependencies
    filter_factory = Mock()
    filter_algorithm = Mock()
    filter_factory.create_factory.return_value = filter_algorithm
    filter_algorithm.do_algorithm.return_value = {"template1", "template2"}

    place_manager = Mock()
    place_manager.get_place_categories.return_value = {"category1", "category2"}
    place_manager_factory = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    random_place_template_factory = Mock()
    text_product = Mock(spec=TextProduct)
    text_product.is_valid.return_value = True
    text_product.get.return_value = "selected_template"
    random_place_template_factory.create_place.return_value = text_product

    command_provider = Mock()
    command = Mock()
    command_provider.create_command.return_value = command

    create_map_entry_command_provider_factory = Mock()
    create_map_entry_command_provider_factory.create_provider.return_value = (
        command_provider
    )

    factories_config = Mock(
        filter_out_used_templates_algorithm_factory=filter_factory,
        place_manager_factory=place_manager_factory,
        random_place_template_based_on_categories_factory=random_place_template_factory,
        create_map_entry_for_playthrough_command_provider_factory=create_map_entry_command_provider_factory,
    )
    return factories_config


@pytest.fixture
def filesystem_manager():
    return Mock(spec=FilesystemManager)


@pytest.fixture
def provider(provider_config, factories_config, filesystem_manager):
    return ConcreteRandomPlaceTypeMapEntryProvider(
        config=provider_config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
    )


# Test Cases


def test_create_map_entry_success(provider, factories_config):
    # Arrange
    result = provider.create_map_entry()

    # Assert
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    factories_config.filter_out_used_templates_algorithm_factory.create_factory.assert_called_once_with(
        "PLACE_TYPE"
    )
    factories_config.filter_out_used_templates_algorithm_factory.create_factory.return_value.do_algorithm.assert_called_once()
    factories_config.random_place_template_based_on_categories_factory.create_place.assert_called_once()
    factories_config.create_map_entry_for_playthrough_command_provider_factory.create_provider.assert_called_once_with(
        "father_id", "PLACE_TYPE"
    )
    factories_config.create_map_entry_for_playthrough_command_provider_factory.create_provider.return_value.create_command.assert_called_once_with(
        "selected_template"
    )
    factories_config.create_map_entry_for_playthrough_command_provider_factory.create_provider.return_value.create_command.return_value.execute.assert_called_once()


def test_create_map_entry_no_available_templates(provider, factories_config):
    # Arrange
    factories_config.filter_out_used_templates_algorithm_factory.create_factory.return_value.do_algorithm.return_value = (
        {}
    )

    # Act
    result = provider.create_map_entry()

    # Assert
    assert (
        result.get_result_type()
        == RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
    )
    factories_config.filter_out_used_templates_algorithm_factory.create_factory.assert_called_once_with(
        "PLACE_TYPE"
    )
    factories_config.filter_out_used_templates_algorithm_factory.create_factory.return_value.do_algorithm.assert_called_once()
    # Ensure that other factories are not called
    factories_config.random_place_template_based_on_categories_factory.create_place.assert_not_called()
    factories_config.create_map_entry_for_playthrough_command_provider_factory.create_provider.assert_not_called()


def test_create_map_entry_invalid_template_product(provider, factories_config):
    # Arrange
    text_product = (
        factories_config.random_place_template_based_on_categories_factory.create_place.return_value
    )
    text_product.is_valid.return_value = False
    text_product.get_error.return_value = "Invalid template error."

    # Act
    result = provider.create_map_entry()

    # Assert
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert (
        result.get_error()
        == "Failed to produce a PLACE_TYPE template: Invalid template error."
    )
    factories_config.create_map_entry_for_playthrough_command_provider_factory.create_provider.assert_not_called()


def test_create_map_entry_exception_handling(provider, factories_config, caplog):
    # Arrange
    factories_config.filter_out_used_templates_algorithm_factory.create_factory.side_effect = Exception(
        "Unexpected error"
    )

    # Act
    result = provider.create_map_entry()

    # Assert
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert result.get_error() == "Unexpected error"
    # Check that the exception was logged
    assert "An error occurred while creating map entry." in caplog.text


def test_create_map_entry_command_execution_failure(provider, factories_config):
    # Arrange
    factories_config.create_map_entry_for_playthrough_command_provider_factory.create_provider.return_value.create_command.return_value.execute.side_effect = Exception(
        "Command execution failed"
    )

    # Act
    result = provider.create_map_entry()

    # Assert
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert result.get_error() == "Command execution failed"


def test_init_with_filesystem_manager(provider_config, factories_config):
    # Arrange
    filesystem_manager = Mock(spec=FilesystemManager)
    provider = ConcreteRandomPlaceTypeMapEntryProvider(
        config=provider_config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
    )

    # Act
    assert provider._filesystem_manager == filesystem_manager


def test_init_without_filesystem_manager(provider_config, factories_config):
    # Arrange
    with patch(
        "src.maps.providers.concrete_random_place_type_map_entry_provider.FilesystemManager"
    ) as MockFilesystemManager:
        mock_filesystem_manager_instance = MockFilesystemManager.return_value
        provider = ConcreteRandomPlaceTypeMapEntryProvider(
            config=provider_config,
            factories_config=factories_config,
            filesystem_manager=None,
        )

    # Act & Assert
    MockFilesystemManager.assert_called_once()
    assert provider._filesystem_manager == mock_filesystem_manager_instance


def test_create_map_entry_template_product_creation_failure(provider, factories_config):
    # Arrange
    factories_config.random_place_template_based_on_categories_factory.create_place.return_value.is_valid.return_value = (
        False
    )
    factories_config.random_place_template_based_on_categories_factory.create_place.return_value.get_error.return_value = (
        "Template creation failed."
    )

    # Act
    result = provider.create_map_entry()

    # Assert
    assert (
        result.get_result_type() == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert (
        result.get_error()
        == "Failed to produce a PLACE_TYPE template: Template creation failed."
    )
    factories_config.create_map_entry_for_playthrough_command_provider_factory.create_provider.assert_not_called()


def test_create_map_entry_multiple_calls(provider, factories_config):
    # Arrange
    # First call succeeds
    result1 = provider.create_map_entry()
    assert (
        result1.get_result_type()
        == RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )

    # Second call with no available templates
    factories_config.filter_out_used_templates_algorithm_factory.create_factory.return_value.do_algorithm.return_value = (
        {}
    )
    result2 = provider.create_map_entry()
    assert (
        result2.get_result_type()
        == RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
    )

    # Third call with invalid template
    factories_config.filter_out_used_templates_algorithm_factory.create_factory.return_value.do_algorithm.return_value = {
        "template3"
    }
    factories_config.random_place_template_based_on_categories_factory.create_place.return_value.is_valid.return_value = (
        False
    )
    factories_config.random_place_template_based_on_categories_factory.create_place.return_value.get_error.return_value = (
        "Invalid template."
    )

    result3 = provider.create_map_entry()
    assert (
        result3.get_result_type()
        == RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    assert (
        result3.get_error()
        == "Failed to produce a PLACE_TYPE template: Invalid template."
    )
