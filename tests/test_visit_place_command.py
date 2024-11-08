# test_visit_place_command.py

from unittest.mock import Mock, patch

import pytest

from src.base.enums import TemplateType
from src.movements.commands.visit_place_command import VisitPlaceCommand


def test_visit_place_command_updates_current_place():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    # Mock dependencies
    process_first_visit_to_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    time_manager = Mock()
    config_loader = Mock()

    # Mock the place manager
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager_factory.create_place_manager.return_value = place_manager

    command = VisitPlaceCommand(
        playthrough_name,
        place_identifier,
        process_first_visit_to_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        time_manager,
        config_loader,
    )

    command.execute()

    playthrough_manager.update_current_place.assert_called_once_with(place_identifier)


def test_visit_place_command_processes_first_visit():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    # Mock dependencies
    process_first_visit_to_place_command_factory = Mock()
    first_visit_command = Mock()
    process_first_visit_to_place_command_factory.create_command.return_value = (
        first_visit_command
    )

    place_manager_factory = Mock()
    playthrough_manager = Mock()
    time_manager = Mock()
    config_loader = Mock()

    # Mock the place manager
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager.is_visited.return_value = False
    place_manager_factory.create_place_manager.return_value = place_manager

    command = VisitPlaceCommand(
        playthrough_name,
        place_identifier,
        process_first_visit_to_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        time_manager,
        config_loader,
    )

    command.execute()

    # Check that the first visit command was created and executed
    process_first_visit_to_place_command_factory.create_command.assert_called_once_with(
        place_identifier
    )
    first_visit_command.execute.assert_called_once()


def test_visit_place_command_does_not_process_first_visit_if_already_visited():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    # Mock dependencies
    process_first_visit_to_place_command_factory = Mock()
    first_visit_command = Mock()
    process_first_visit_to_place_command_factory.create_command.return_value = (
        first_visit_command
    )

    place_manager_factory = Mock()
    playthrough_manager = Mock()
    time_manager = Mock()
    config_loader = Mock()

    # Mock the place manager
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager.is_visited.return_value = True
    place_manager_factory.create_place_manager.return_value = place_manager

    command = VisitPlaceCommand(
        playthrough_name,
        place_identifier,
        process_first_visit_to_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        time_manager,
        config_loader,
    )

    command.execute()

    # Check that the first visit command was not created nor executed
    process_first_visit_to_place_command_factory.create_command.assert_not_called()
    first_visit_command.execute.assert_not_called()


def test_visit_place_command_does_not_process_first_visit_if_origin_is_room():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    # Mock dependencies
    process_first_visit_to_place_command_factory = Mock()
    first_visit_command = Mock()
    process_first_visit_to_place_command_factory.create_command.return_value = (
        first_visit_command
    )

    place_manager_factory = Mock()
    playthrough_manager = Mock()
    time_manager = Mock()
    config_loader = Mock()

    # Mock the place manager
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = (
        TemplateType.ROOM
    )  # Origin is ROOM
    place_manager.is_visited.return_value = False
    place_manager_factory.create_place_manager.return_value = place_manager

    command = VisitPlaceCommand(
        playthrough_name,
        place_identifier,
        process_first_visit_to_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        time_manager,
        config_loader,
    )

    command.execute()

    # Check that the first visit command was not created nor executed
    process_first_visit_to_place_command_factory.create_command.assert_not_called()
    first_visit_command.execute.assert_not_called()


def test_visit_place_command_does_not_process_first_visit_if_destination_is_room():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    # Mock dependencies
    process_first_visit_to_place_command_factory = Mock()
    first_visit_command = Mock()
    process_first_visit_to_place_command_factory.create_command.return_value = (
        first_visit_command
    )

    place_manager_factory = Mock()
    playthrough_manager = Mock()
    time_manager = Mock()
    config_loader = Mock()

    # Mock the place manager
    place_manager = Mock()

    # Define side_effect for get_current_place_type
    # First call returns LOCATION (origin), second call returns ROOM (destination)
    place_manager.get_current_place_type.side_effect = [
        TemplateType.LOCATION,
        TemplateType.ROOM,
    ]
    place_manager.is_visited.return_value = False
    place_manager_factory.create_place_manager.return_value = place_manager

    command = VisitPlaceCommand(
        playthrough_name,
        place_identifier,
        process_first_visit_to_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        time_manager,
        config_loader,
    )

    command.execute()

    # Check that the first visit command was not created nor executed
    process_first_visit_to_place_command_factory.create_command.assert_not_called()
    first_visit_command.execute.assert_not_called()


def test_visit_place_command_advances_time_correctly():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    # Mock dependencies
    process_first_visit_to_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    time_manager = Mock()
    config_loader = Mock()

    time_to_advance = 5
    config_loader.get_time_advanced_due_to_exiting_location.return_value = (
        time_to_advance
    )

    # Mock the place manager
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager.is_visited.return_value = (
        True  # So that first visit command is not processed
    )
    place_manager_factory.create_place_manager.return_value = place_manager

    command = VisitPlaceCommand(
        playthrough_name,
        place_identifier,
        process_first_visit_to_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        time_manager,
        config_loader,
    )

    command.execute()

    time_manager.advance_time.assert_called_once_with(time_to_advance)


def test_visit_place_command_validates_non_empty_strings():
    process_first_visit_to_place_command_factory = Mock()
    place_manager_factory = Mock()

    with pytest.raises(ValueError):
        VisitPlaceCommand(
            "",  # Empty playthrough_name
            "place_1",
            process_first_visit_to_place_command_factory,
            place_manager_factory,
        )

    with pytest.raises(ValueError):
        VisitPlaceCommand(
            "playthrough_name",
            "",  # Empty place_identifier
            process_first_visit_to_place_command_factory,
            place_manager_factory,
        )


def test_visit_place_command_uses_default_playthrough_manager_if_none_provided():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    process_first_visit_to_place_command_factory = Mock()
    place_manager_factory = Mock()
    time_manager = Mock()
    config_loader = Mock()

    with patch(
        "src.movements.commands.visit_place_command.PlaythroughManager"
    ) as MockPlaythroughManager:
        command = VisitPlaceCommand(
            playthrough_name,
            place_identifier,
            process_first_visit_to_place_command_factory,
            place_manager_factory,
            playthrough_manager=None,
            time_manager=time_manager,
            config_loader=config_loader,
        )

        MockPlaythroughManager.assert_called_once_with(playthrough_name)
        assert command._playthrough_manager == MockPlaythroughManager.return_value


def test_visit_place_command_uses_default_time_manager_if_none_provided():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    process_first_visit_to_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    config_loader = Mock()

    with patch(
        "src.movements.commands.visit_place_command.TimeManager"
    ) as MockTimeManager:
        command = VisitPlaceCommand(
            playthrough_name,
            place_identifier,
            process_first_visit_to_place_command_factory,
            place_manager_factory,
            playthrough_manager=playthrough_manager,
            time_manager=None,
            config_loader=config_loader,
        )

        MockTimeManager.assert_called_once_with(playthrough_name)
        assert command._time_manager == MockTimeManager.return_value


def test_visit_place_command_uses_default_config_loader_if_none_provided():
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    process_first_visit_to_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    time_manager = Mock()

    with patch(
        "src.movements.commands.visit_place_command.ConfigLoader"
    ) as MockConfigLoader:
        command = VisitPlaceCommand(
            playthrough_name,
            place_identifier,
            process_first_visit_to_place_command_factory,
            place_manager_factory,
            playthrough_manager=playthrough_manager,
            time_manager=time_manager,
            config_loader=None,
        )

        MockConfigLoader.assert_called_once()
        assert command._config_loader == MockConfigLoader.return_value


@pytest.mark.parametrize(
    "origin_type, destination_type, is_visited, should_process_first_visit",
    [
        (TemplateType.LOCATION, TemplateType.LOCATION, False, True),
        (TemplateType.LOCATION, TemplateType.LOCATION, True, False),
        (TemplateType.ROOM, TemplateType.LOCATION, False, False),
        (TemplateType.LOCATION, TemplateType.ROOM, False, False),
        (TemplateType.ROOM, TemplateType.ROOM, False, False),
        (TemplateType.LOCATION, TemplateType.AREA, False, True),
        (TemplateType.AREA, TemplateType.REGION, False, True),
    ],
)
def test_visit_place_command_first_visit_processing(
    origin_type, destination_type, is_visited, should_process_first_visit
):
    playthrough_name = "test_playthrough"
    place_identifier = "place_1"

    # Mock dependencies
    process_first_visit_to_place_command_factory = Mock()
    first_visit_command = Mock()
    process_first_visit_to_place_command_factory.create_command.return_value = (
        first_visit_command
    )

    place_manager_factory = Mock()
    playthrough_manager = Mock()
    time_manager = Mock()
    config_loader = Mock()

    # Mock the place manager
    place_manager = Mock()

    # Define side_effect for get_current_place_type
    # First call returns origin_type, second call returns destination_type
    place_manager.get_current_place_type.side_effect = [origin_type, destination_type]
    place_manager.is_visited.return_value = is_visited
    place_manager_factory.create_place_manager.return_value = place_manager

    command = VisitPlaceCommand(
        playthrough_name,
        place_identifier,
        process_first_visit_to_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        time_manager,
        config_loader,
    )

    command.execute()

    if should_process_first_visit:
        process_first_visit_to_place_command_factory.create_command.assert_called_once_with(
            place_identifier
        )
        first_visit_command.execute.assert_called_once()
    else:
        process_first_visit_to_place_command_factory.create_command.assert_not_called()
        first_visit_command.execute.assert_not_called()
