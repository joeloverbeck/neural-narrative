from unittest.mock import Mock

import pytest

from src.maps.commands.create_initial_map_command import CreateInitialMapCommand
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType


def test_execute_success():
    """Test successful execution of CreateInitialMapCommand."""
    story_universe_template = "Some Universe"
    success_result = Mock()
    success_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    random_provider = Mock()
    random_provider.create_random_place_type_map_entry.return_value = success_result
    random_provider_factory = Mock()
    random_provider_factory.create_provider.return_value = random_provider
    map_manager = Mock()
    (map_manager.get_identifier_and_place_template_of_latest_map_entry.side_effect) = [
        ("world_id", "world_template"),
        ("region_id", "region_template"),
    ]
    map_manager_factory = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager
    command = CreateInitialMapCommand(
        story_universe_template=story_universe_template,
        random_template_type_map_entry_provider_factory=random_provider_factory,
        map_manager_factory=map_manager_factory,
    )
    command.execute()
    assert random_provider_factory.create_provider.call_count == 3
    assert random_provider.create_random_place_type_map_entry.call_count == 3
    assert map_manager_factory.create_map_manager.call_count == 2
    assert (
        map_manager.get_identifier_and_place_template_of_latest_map_entry.call_count
        == 2
    )


def test_execute_world_creation_failure():
    """Test failure during world creation."""
    story_universe_template = "Some Universe"
    failure_result = Mock()
    failure_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    failure_result.get_error.return_value = "World creation failed"
    random_provider = Mock()
    random_provider.create_random_place_type_map_entry.return_value = failure_result
    random_provider_factory = Mock()
    random_provider_factory.create_provider.return_value = random_provider
    map_manager_factory = Mock()
    command = CreateInitialMapCommand(
        story_universe_template=story_universe_template,
        random_template_type_map_entry_provider_factory=random_provider_factory,
        map_manager_factory=map_manager_factory,
    )
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert "Was unable to create a map entry for a world" in str(exc_info)
    assert random_provider.create_random_place_type_map_entry.call_count == 1


def test_execute_region_creation_failure():
    """Test failure during region creation."""
    story_universe_template = "Some Universe"
    success_result = Mock()
    success_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    failure_result = Mock()
    failure_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    failure_result.get_error.return_value = "Region creation failed"
    random_provider = Mock()
    random_provider.create_random_place_type_map_entry.side_effect = [
        success_result,
        failure_result,
    ]
    random_provider_factory = Mock()
    random_provider_factory.create_provider.return_value = random_provider
    map_manager = Mock()
    (map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value) = (
        "world_id",
        "world_template",
    )
    map_manager_factory = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager
    command = CreateInitialMapCommand(
        story_universe_template=story_universe_template,
        random_template_type_map_entry_provider_factory=random_provider_factory,
        map_manager_factory=map_manager_factory,
    )
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert "Was unable to create a map entry for a region" in str(exc_info)
    assert random_provider.create_random_place_type_map_entry.call_count == 2


def test_execute_area_creation_failure():
    """Test failure during area creation."""
    story_universe_template = "Some Universe"
    success_result = Mock()
    success_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    failure_result = Mock()
    failure_result.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    failure_result.get_error.return_value = "Area creation failed"
    random_provider = Mock()
    random_provider.create_random_place_type_map_entry.side_effect = [
        success_result,
        success_result,
        failure_result,
    ]
    random_provider_factory = Mock()
    random_provider_factory.create_provider.return_value = random_provider
    map_manager = Mock()
    (map_manager.get_identifier_and_place_template_of_latest_map_entry.side_effect) = [
        ("world_id", "world_template"),
        ("region_id", "region_template"),
    ]
    map_manager_factory = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager
    command = CreateInitialMapCommand(
        story_universe_template=story_universe_template,
        random_template_type_map_entry_provider_factory=random_provider_factory,
        map_manager_factory=map_manager_factory,
    )
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert "Was unable to create a map entry for an area" in str(exc_info)
    assert random_provider.create_random_place_type_map_entry.call_count == 3
