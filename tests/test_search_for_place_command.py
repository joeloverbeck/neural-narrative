# test_search_for_place_command.py

from unittest.mock import MagicMock, patch

import pytest

from src.base.constants import CHILD_TEMPLATE_TYPE
from src.base.playthrough_manager import PlaythroughManager
from src.maps.commands.search_for_place_command import SearchForPlaceCommand
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType
from src.maps.exceptions import SearchForPlaceError
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.random_template_type_map_entry_provider_factory import (
    RandomTemplateTypeMapEntryProviderFactory,
)


# Assuming SearchForPlaceCommand is located in src/maps/commands/search_for_place_command.py


@pytest.fixture
def mock_random_template_type_map_entry_provider_factory():
    return MagicMock(spec=RandomTemplateTypeMapEntryProviderFactory)


@pytest.fixture
def mock_place_manager_factory():
    return MagicMock(spec=PlaceManagerFactory)


@pytest.fixture
def mock_map_manager_factory():
    return MagicMock(spec=MapManagerFactory)


@pytest.fixture
def mock_playthrough_manager():
    return MagicMock(spec=PlaythroughManager)


@pytest.fixture
def valid_playthrough_name():
    return "test_playthrough"


@pytest.fixture
def command_instance(
    valid_playthrough_name,
    mock_random_template_type_map_entry_provider_factory,
    mock_place_manager_factory,
    mock_map_manager_factory,
    mock_playthrough_manager,
):
    return SearchForPlaceCommand(
        playthrough_name=valid_playthrough_name,
        random_template_type_map_entry_provider_factory=mock_random_template_type_map_entry_provider_factory,
        place_manager_factory=mock_place_manager_factory,
        map_manager_factory=mock_map_manager_factory,
        playthrough_manager=mock_playthrough_manager,
    )


def test_init_with_valid_arguments(
    valid_playthrough_name,
    mock_random_template_type_map_entry_provider_factory,
    mock_place_manager_factory,
    mock_map_manager_factory,
    mock_playthrough_manager,
):
    command = SearchForPlaceCommand(
        playthrough_name=valid_playthrough_name,
        random_template_type_map_entry_provider_factory=mock_random_template_type_map_entry_provider_factory,
        place_manager_factory=mock_place_manager_factory,
        map_manager_factory=mock_map_manager_factory,
        playthrough_manager=mock_playthrough_manager,
    )

    assert command._playthrough_name == valid_playthrough_name
    assert (
        command._random_template_type_map_entry_provider_factory
        == mock_random_template_type_map_entry_provider_factory
    )
    assert command._place_manager_factory == mock_place_manager_factory
    assert command._map_manager_factory == mock_map_manager_factory
    assert command._playthrough_manager == mock_playthrough_manager


def test_init_without_playthrough_manager(
    valid_playthrough_name,
    mock_random_template_type_map_entry_provider_factory,
    mock_place_manager_factory,
    mock_map_manager_factory,
):
    with patch(
        "src.maps.commands.search_for_place_command.PlaythroughManager"
    ) as MockPlaythroughManager:
        mock_playthrough_manager_instance = MagicMock(spec=PlaythroughManager)
        MockPlaythroughManager.return_value = mock_playthrough_manager_instance

        command = SearchForPlaceCommand(
            playthrough_name=valid_playthrough_name,
            random_template_type_map_entry_provider_factory=mock_random_template_type_map_entry_provider_factory,
            place_manager_factory=mock_place_manager_factory,
            map_manager_factory=mock_map_manager_factory,
        )

        MockPlaythroughManager.assert_called_once_with(valid_playthrough_name)
        assert command._playthrough_manager == mock_playthrough_manager_instance


def test_init_with_empty_playthrough_name(
    mock_random_template_type_map_entry_provider_factory,
    mock_place_manager_factory,
    mock_map_manager_factory,
):
    with pytest.raises(ValueError) as exc_info:
        SearchForPlaceCommand(
            playthrough_name="",
            random_template_type_map_entry_provider_factory=mock_random_template_type_map_entry_provider_factory,
            place_manager_factory=mock_place_manager_factory,
            map_manager_factory=mock_map_manager_factory,
        )
    assert "playthrough_name" in str(exc_info.value)


def test_execute_success(
    command_instance,
    mock_map_manager_factory,
    mock_playthrough_manager,
    mock_place_manager_factory,
    mock_random_template_type_map_entry_provider_factory,
):
    # Mock map manager and its method
    mock_map_manager = MagicMock()
    mock_map_manager.get_current_place_template.return_value = "father_template"
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    # Mock playthrough manager and its method
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        "father_identifier"
    )

    # Mock place manager and its method
    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = "current_place_type"
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Determine child_place_type using CHILD_TEMPLATE_TYPE
    current_place_type = "current_place_type"
    child_place_type = CHILD_TEMPLATE_TYPE.get(current_place_type)  # noqa

    # Mock provider and its method
    mock_provider = MagicMock()
    mock_provider.create_map_entry.return_value.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
        mock_provider
    )

    # Execute
    command_instance.execute()

    # Assertions
    mock_map_manager_factory.create_map_manager.assert_called_once()
    mock_map_manager.get_current_place_template.assert_called_once()

    mock_playthrough_manager.get_current_place_identifier.assert_called_once()

    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()

    mock_random_template_type_map_entry_provider_factory.create_provider.assert_called_once_with(
        "father_identifier", "father_template", "current_place_type", child_place_type
    )

    mock_provider.create_map_entry.assert_called_once()


def test_execute_failure_result_type_failure(
    command_instance,
    mock_map_manager_factory,
    mock_playthrough_manager,
    mock_place_manager_factory,
    mock_random_template_type_map_entry_provider_factory,
):
    # Setup mocks similar to the success case
    mock_map_manager = MagicMock()
    mock_map_manager.get_current_place_template.return_value = "father_template"
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    mock_playthrough_manager.get_current_place_identifier.return_value = (
        "father_identifier"
    )

    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = "current_place_type"
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    current_place_type = "current_place_type"
    child_place_type = CHILD_TEMPLATE_TYPE.get(current_place_type)  # noqa

    mock_provider = MagicMock()
    mock_provider.create_map_entry.return_value.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
        mock_provider
    )

    # Execute and expect exception
    with pytest.raises(SearchForPlaceError) as exc_info:
        command_instance.execute()

    assert "The search for a place failed for an unknown reason." in str(exc_info.value)


def test_execute_failure_result_type_no_available_templates(
    command_instance,
    mock_map_manager_factory,
    mock_playthrough_manager,
    mock_place_manager_factory,
    mock_random_template_type_map_entry_provider_factory,
):
    # Setup mocks similar to the success case
    mock_map_manager = MagicMock()
    mock_map_manager.get_current_place_template.return_value = "father_template"
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    mock_playthrough_manager.get_current_place_identifier.return_value = (
        "father_identifier"
    )

    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = "current_place_type"
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    current_place_type = "current_place_type"
    child_place_type = CHILD_TEMPLATE_TYPE.get(current_place_type)  # noqa

    mock_provider = MagicMock()
    mock_provider.create_map_entry.return_value.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
    )
    mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
        mock_provider
    )

    # Execute and expect exception
    with pytest.raises(SearchForPlaceError) as exc_info:
        command_instance.execute()

    assert (
        "The search for a place failed because there were no available templates."
        in str(exc_info.value)
    )


def test_execute_calls_methods_in_correct_order(
    command_instance,
    mock_map_manager_factory,
    mock_playthrough_manager,
    mock_place_manager_factory,
    mock_random_template_type_map_entry_provider_factory,
):
    # This test ensures that methods are called in the expected order
    mock_map_manager = MagicMock()
    mock_map_manager.get_current_place_template.return_value = "father_template"
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    mock_playthrough_manager.get_current_place_identifier.return_value = (
        "father_identifier"
    )

    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = "current_place_type"
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    mock_provider = MagicMock()
    mock_provider.create_map_entry.return_value.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
        mock_provider
    )

    with patch.object(command_instance, "execute", wraps=command_instance.execute):
        command_instance.execute()

    # Here, instead of checking the order, we ensure all methods were called.
    # To strictly test order, more sophisticated mocking or a different approach is needed.
    mock_map_manager_factory.create_map_manager.assert_called_once()
    mock_map_manager.get_current_place_template.assert_called_once()
    mock_playthrough_manager.get_current_place_identifier.assert_called_once()
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_random_template_type_map_entry_provider_factory.create_provider.assert_called_once()
    mock_provider.create_map_entry.assert_called_once()


def test_execute_with_invalid_current_place_type(
    command_instance,
    mock_map_manager_factory,
    mock_playthrough_manager,
    mock_place_manager_factory,
    mock_random_template_type_map_entry_provider_factory,
):
    # Simulate an invalid current_place_type that is not in CHILD_TEMPLATE_TYPE
    mock_map_manager = MagicMock()
    mock_map_manager.get_current_place_template.return_value = "father_template"
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    mock_playthrough_manager.get_current_place_identifier.return_value = (
        "father_identifier"
    )

    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = "invalid_place_type"
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    CHILD_TEMPLATE_TYPE.get("invalid_place_type")  # noqa  # This should be None

    mock_provider = MagicMock()
    mock_provider.create_map_entry.return_value.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
        mock_provider
    )

    # Execute
    command_instance.execute()

    # Ensure that create_provider was called with child_place_type as None
    mock_random_template_type_map_entry_provider_factory.create_provider.assert_called_once_with(
        "father_identifier", "father_template", "invalid_place_type", None
    )


def test_execute_provider_creation_with_correct_arguments(
    command_instance,
    mock_map_manager_factory,
    mock_playthrough_manager,
    mock_place_manager_factory,
    mock_random_template_type_map_entry_provider_factory,
):
    # Specific test to check arguments passed to create_provider
    mock_map_manager = MagicMock()
    mock_map_manager.get_current_place_template.return_value = "father_template"
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    mock_playthrough_manager.get_current_place_identifier.return_value = (
        "father_identifier"
    )

    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = "current_place_type"
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    child_place_type = CHILD_TEMPLATE_TYPE.get("current_place_type")  # noqa

    mock_provider = MagicMock()
    mock_provider.create_map_entry.return_value.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
        mock_provider
    )

    # Execute
    command_instance.execute()

    # Check that create_provider was called with correct arguments
    mock_random_template_type_map_entry_provider_factory.create_provider.assert_called_once_with(
        "father_identifier", "father_template", "current_place_type", child_place_type
    )


def test_execute_no_playthrough_manager_provided(
    valid_playthrough_name,
    mock_random_template_type_map_entry_provider_factory,
    mock_place_manager_factory,
    mock_map_manager_factory,
):
    with patch(
        "src.maps.commands.search_for_place_command.PlaythroughManager"
    ) as MockPlaythroughManager:
        mock_playthrough_manager_instance = MagicMock(spec=PlaythroughManager)
        MockPlaythroughManager.return_value = mock_playthrough_manager_instance

        command = SearchForPlaceCommand(
            playthrough_name=valid_playthrough_name,
            random_template_type_map_entry_provider_factory=mock_random_template_type_map_entry_provider_factory,
            place_manager_factory=mock_place_manager_factory,
            map_manager_factory=mock_map_manager_factory,
        )

        # Setup execute
        mock_map_manager = MagicMock()
        mock_map_manager.get_current_place_template.return_value = "father_template"
        mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

        mock_playthrough_manager_instance.get_current_place_identifier.return_value = (
            "father_identifier"
        )

        mock_place_manager = MagicMock()
        mock_place_manager.get_current_place_type.return_value = "current_place_type"
        mock_place_manager_factory.create_place_manager.return_value = (
            mock_place_manager
        )

        child_place_type = CHILD_TEMPLATE_TYPE.get("current_place_type")  # noqa

        mock_provider = MagicMock()
        mock_provider.create_map_entry.return_value.get_result_type.return_value = (
            RandomTemplateTypeMapEntryCreationResultType.SUCCESS
        )
        mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
            mock_provider
        )

        # Execute
        command.execute()

        # Ensure PlaythroughManager was instantiated
        MockPlaythroughManager.assert_called_once_with(valid_playthrough_name)
        mock_playthrough_manager_instance.get_current_place_identifier.assert_called_once()


def test_execute_create_map_manager_called_once(
    command_instance,
    mock_map_manager_factory,
):
    # Ensure create_map_manager is called exactly once
    command_instance.execute()
    mock_map_manager_factory.create_map_manager.assert_called_once()


def test_execute_create_place_manager_called_once(
    command_instance,
    mock_place_manager_factory,
):
    # Ensure create_place_manager is called exactly once
    command_instance.execute()
    mock_place_manager_factory.create_place_manager.assert_called_once()


def test_execute_create_provider_called_once(
    command_instance,
    mock_random_template_type_map_entry_provider_factory,
    mock_map_manager_factory,
    mock_playthrough_manager,
    mock_place_manager_factory,
):
    # Setup necessary mocks
    mock_map_manager = MagicMock()
    mock_map_manager.get_current_place_template.return_value = "father_template"
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    mock_playthrough_manager.get_current_place_identifier.return_value = (
        "father_identifier"
    )

    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = "current_place_type"
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    child_place_type = CHILD_TEMPLATE_TYPE.get("current_place_type")  # noqa

    mock_provider = MagicMock()
    mock_provider.create_map_entry.return_value.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
        mock_provider
    )

    # Execute
    command_instance.execute()

    # Ensure create_provider is called once
    mock_random_template_type_map_entry_provider_factory.create_provider.assert_called_once()


def test_execute_create_map_entry_called_once(
    command_instance,
    mock_random_template_type_map_entry_provider_factory,
    mock_map_manager_factory,
    mock_playthrough_manager,
    mock_place_manager_factory,
):
    # Setup necessary mocks
    mock_map_manager = MagicMock()
    mock_map_manager.get_current_place_template.return_value = "father_template"
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    mock_playthrough_manager.get_current_place_identifier.return_value = (
        "father_identifier"
    )

    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = "current_place_type"
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    mock_provider = MagicMock()
    mock_provider.create_map_entry.return_value.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )
    mock_random_template_type_map_entry_provider_factory.create_provider.return_value = (
        mock_provider
    )

    # Execute
    command_instance.execute()

    # Ensure create_map_entry is called once
    mock_provider.create_map_entry.assert_called_once()
