from unittest.mock import Mock

import pytest

from src.base.required_string import RequiredString
from src.maps.commands.create_initial_map_command import CreateInitialMapCommand
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType


def test_execute_success():
    """Test successful execution of CreateInitialMapCommand."""

    # Mock the required string
    story_universe_template = RequiredString("Some Universe")

    # Mock a successful result for all creations
    success_result = Mock()
    success_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )

    # Mock the RandomTemplateTypeMapEntryProvider
    random_provider = Mock()
    random_provider.create_random_place_type_map_entry.return_value = success_result

    # Mock the RandomTemplateTypeMapEntryProviderFactory
    random_provider_factory = Mock()
    random_provider_factory.create_provider.return_value = random_provider

    # Mock the MapManager
    map_manager = Mock()
    map_manager.get_identifier_and_place_template_of_latest_map_entry.side_effect = [
        ("world_id", "world_template"),
        ("region_id", "region_template"),
    ]

    # Mock the MapManagerFactory
    map_manager_factory = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager

    # Instantiate the command
    command = CreateInitialMapCommand(
        story_universe_template=story_universe_template,
        random_template_type_map_entry_provider_factory=random_provider_factory,
        map_manager_factory=map_manager_factory,
    )

    # Execute the command
    command.execute()

    # Assertions to verify interactions
    assert (
        random_provider_factory.create_provider.call_count == 3
    )  # world, region, area
    assert random_provider.create_random_place_type_map_entry.call_count == 3
    assert map_manager_factory.create_map_manager.call_count == 2  # For region and area
    assert (
        map_manager.get_identifier_and_place_template_of_latest_map_entry.call_count
        == 2
    )


def test_execute_world_creation_failure():
    """Test failure during world creation."""

    # Mock the required string
    story_universe_template = RequiredString("Some Universe")

    # Mock a failure result for world creation
    failure_result = Mock()
    failure_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    failure_result.get_error.return_value = "World creation failed"

    # Mock the RandomTemplateTypeMapEntryProvider
    random_provider = Mock()
    random_provider.create_random_place_type_map_entry.return_value = failure_result

    # Mock the RandomTemplateTypeMapEntryProviderFactory
    random_provider_factory = Mock()
    random_provider_factory.create_provider.return_value = random_provider

    # MapManagerFactory is not needed since world creation fails
    map_manager_factory = Mock()

    # Instantiate the command
    command = CreateInitialMapCommand(
        story_universe_template=story_universe_template,
        random_template_type_map_entry_provider_factory=random_provider_factory,
        map_manager_factory=map_manager_factory,
    )

    # Execute the command and expect a ValueError
    with pytest.raises(ValueError) as exc_info:
        command.execute()

    # Verify the error message
    assert "Was unable to create a map entry for a world" in str(exc_info.value)

    # Verify that only world creation was attempted
    assert random_provider.create_random_place_type_map_entry.call_count == 1


def test_execute_region_creation_failure():
    """Test failure during region creation."""

    # Mock the required string
    story_universe_template = RequiredString("Some Universe")

    # Mock a successful result for world creation
    success_result = Mock()
    success_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )

    # Mock a failure result for region creation
    failure_result = Mock()
    failure_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    failure_result.get_error.return_value = "Region creation failed"

    # Mock the RandomTemplateTypeMapEntryProvider
    random_provider = Mock()
    # First call succeeds (world), second call fails (region)
    random_provider.create_random_place_type_map_entry.side_effect = [
        success_result,
        failure_result,
    ]

    # Mock the RandomTemplateTypeMapEntryProviderFactory
    random_provider_factory = Mock()
    random_provider_factory.create_provider.return_value = random_provider

    # Mock the MapManager
    map_manager = Mock()
    map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value = (
        "world_id",
        "world_template",
    )

    # Mock the MapManagerFactory
    map_manager_factory = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager

    # Instantiate the command
    command = CreateInitialMapCommand(
        story_universe_template=story_universe_template,
        random_template_type_map_entry_provider_factory=random_provider_factory,
        map_manager_factory=map_manager_factory,
    )

    # Execute the command and expect a ValueError
    with pytest.raises(ValueError) as exc_info:
        command.execute()

    # Verify the error message
    assert "Was unable to create a map entry for a region" in str(exc_info.value)

    # Verify that world and region creation were attempted
    assert random_provider.create_random_place_type_map_entry.call_count == 2


def test_execute_area_creation_failure():
    """Test failure during area creation."""

    # Mock the required string
    story_universe_template = RequiredString("Some Universe")

    # Mock a successful result for world and region creation
    success_result = Mock()
    success_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )

    # Mock a failure result for area creation
    failure_result = Mock()
    failure_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    failure_result.get_error.return_value = "Area creation failed"

    # Mock the RandomTemplateTypeMapEntryProvider
    random_provider = Mock()
    # First two calls succeed (world and region), third call fails (area)
    random_provider.create_random_place_type_map_entry.side_effect = [
        success_result,
        success_result,
        failure_result,
    ]

    # Mock the RandomTemplateTypeMapEntryProviderFactory
    random_provider_factory = Mock()
    random_provider_factory.create_provider.return_value = random_provider

    # Mock the MapManager
    map_manager = Mock()
    # First call returns world data, second call returns region data
    map_manager.get_identifier_and_place_template_of_latest_map_entry.side_effect = [
        ("world_id", "world_template"),
        ("region_id", "region_template"),
    ]

    # Mock the MapManagerFactory
    map_manager_factory = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager

    # Instantiate the command
    command = CreateInitialMapCommand(
        story_universe_template=story_universe_template,
        random_template_type_map_entry_provider_factory=random_provider_factory,
        map_manager_factory=map_manager_factory,
    )

    # Execute the command and expect a ValueError
    with pytest.raises(ValueError) as exc_info:
        command.execute()

    # Verify the error message
    assert "Was unable to create a map entry for an area" in str(exc_info.value)

    # Verify that world, region, and area creation were attempted
    assert random_provider.create_random_place_type_map_entry.call_count == 3
