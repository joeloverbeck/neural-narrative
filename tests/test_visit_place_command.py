from unittest.mock import Mock, create_autospec, patch

import pytest

from src.base.abstracts.command import Command
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.filesystem.config_loader import ConfigLoader
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.commands.visit_place_command import VisitPlaceCommand
from src.movements.factories.process_first_visit_to_place_command_factory import (
    ProcessFirstVisitToPlaceCommandFactory,
)
from src.time.time_manager import TimeManager


# Helper function to assert that a string is non-empty
def test_validate_non_empty_string_called():
    with patch(
        "src.movements.commands.visit_place_command.validate_non_empty_string"
    ) as mock_validate:
        cmd = VisitPlaceCommand(
            playthrough_name="TestPlaythrough",
            place_identifier="TestPlace",
            process_first_visit_to_place_command_factory=Mock(),
            place_manager_factory=Mock(),
        )
        mock_validate.assert_any_call("TestPlaythrough", "playthrough_name")
        mock_validate.assert_any_call("TestPlace", "place_identifier")


@pytest.fixture
def mock_dependencies():
    process_first_visit_factory = create_autospec(
        ProcessFirstVisitToPlaceCommandFactory
    )
    place_manager_factory = create_autospec(PlaceManagerFactory)
    playthrough_manager = create_autospec(PlaythroughManager)
    time_manager = create_autospec(TimeManager)
    config_loader = create_autospec(ConfigLoader)

    return {
        "process_first_visit_factory": process_first_visit_factory,
        "place_manager_factory": place_manager_factory,
        "playthrough_manager": playthrough_manager,
        "time_manager": time_manager,
        "config_loader": config_loader,
    }


def test_initialization_with_required_dependencies(mock_dependencies):
    cmd = VisitPlaceCommand(
        playthrough_name="TestPlaythrough",
        place_identifier="TestPlace",
        process_first_visit_to_place_command_factory=mock_dependencies[
            "process_first_visit_factory"
        ],
        place_manager_factory=mock_dependencies["place_manager_factory"],
    )

    assert cmd._place_identifier == "TestPlace"
    assert (
        cmd._process_first_visit_to_place_command_factory
        == mock_dependencies["process_first_visit_factory"]
    )
    assert cmd._place_manager_factory == mock_dependencies["place_manager_factory"]
    assert isinstance(cmd._playthrough_manager, PlaythroughManager)
    assert isinstance(cmd._time_manager, TimeManager)
    assert isinstance(cmd._config_loader, ConfigLoader)


def test_initialization_with_all_dependencies(mock_dependencies):
    cmd = VisitPlaceCommand(
        playthrough_name="TestPlaythrough",
        place_identifier="TestPlace",
        process_first_visit_to_place_command_factory=mock_dependencies[
            "process_first_visit_factory"
        ],
        place_manager_factory=mock_dependencies["place_manager_factory"],
        playthrough_manager=mock_dependencies["playthrough_manager"],
        time_manager=mock_dependencies["time_manager"],
        config_loader=mock_dependencies["config_loader"],
    )

    assert cmd._playthrough_manager == mock_dependencies["playthrough_manager"]
    assert cmd._time_manager == mock_dependencies["time_manager"]
    assert cmd._config_loader == mock_dependencies["config_loader"]


def test_execute_room_type(mock_dependencies):
    # Arrange
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.ROOM

    mock_dependencies["place_manager_factory"].create_place_manager.return_value = (
        place_manager
    )

    cmd = VisitPlaceCommand(
        playthrough_name="TestPlaythrough",
        place_identifier="TestPlace",
        process_first_visit_to_place_command_factory=mock_dependencies[
            "process_first_visit_factory"
        ],
        place_manager_factory=mock_dependencies["place_manager_factory"],
        playthrough_manager=mock_dependencies["playthrough_manager"],
        time_manager=mock_dependencies["time_manager"],
        config_loader=mock_dependencies["config_loader"],
    )

    # Act
    cmd.execute()

    # Assert
    mock_dependencies[
        "playthrough_manager"
    ].update_current_place.assert_called_once_with("TestPlace")
    mock_dependencies["place_manager_factory"].create_place_manager.assert_called_once()
    place_manager.get_current_place_type.assert_called_once()
    mock_dependencies["process_first_visit_factory"].create_command.assert_not_called()
    mock_dependencies["time_manager"].advance_time.assert_not_called()


def test_execute_first_visit(mock_dependencies):
    # Arrange
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager.is_visited.return_value = False

    first_visit_command = Mock(spec=Command)
    mock_dependencies["process_first_visit_factory"].create_command.return_value = (
        first_visit_command
    )

    mock_dependencies["place_manager_factory"].create_place_manager.return_value = (
        place_manager
    )
    mock_dependencies[
        "config_loader"
    ].get_time_advanced_due_to_exiting_location.return_value = 10

    cmd = VisitPlaceCommand(
        playthrough_name="TestPlaythrough",
        place_identifier="TestPlace",
        process_first_visit_to_place_command_factory=mock_dependencies[
            "process_first_visit_factory"
        ],
        place_manager_factory=mock_dependencies["place_manager_factory"],
        playthrough_manager=mock_dependencies["playthrough_manager"],
        time_manager=mock_dependencies["time_manager"],
        config_loader=mock_dependencies["config_loader"],
    )

    # Act
    cmd.execute()

    # Assert
    mock_dependencies[
        "playthrough_manager"
    ].update_current_place.assert_called_once_with("TestPlace")
    mock_dependencies["place_manager_factory"].create_place_manager.assert_called_once()
    place_manager.get_current_place_type.assert_called_once()
    place_manager.is_visited.assert_called_once_with("TestPlace")
    mock_dependencies[
        "process_first_visit_factory"
    ].create_command.assert_called_once_with("TestPlace")
    first_visit_command.execute.assert_called_once()
    mock_dependencies[
        "config_loader"
    ].get_time_advanced_due_to_exiting_location.assert_called_once()
    mock_dependencies["time_manager"].advance_time.assert_called_once_with(10)


def test_execute_already_visited(mock_dependencies):
    # Arrange
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager.is_visited.return_value = True

    mock_dependencies["place_manager_factory"].create_place_manager.return_value = (
        place_manager
    )
    mock_dependencies[
        "config_loader"
    ].get_time_advanced_due_to_exiting_location.return_value = 5

    cmd = VisitPlaceCommand(
        playthrough_name="TestPlaythrough",
        place_identifier="TestPlace",
        process_first_visit_to_place_command_factory=mock_dependencies[
            "process_first_visit_factory"
        ],
        place_manager_factory=mock_dependencies["place_manager_factory"],
        playthrough_manager=mock_dependencies["playthrough_manager"],
        time_manager=mock_dependencies["time_manager"],
        config_loader=mock_dependencies["config_loader"],
    )

    # Act
    cmd.execute()

    # Assert
    mock_dependencies[
        "playthrough_manager"
    ].update_current_place.assert_called_once_with("TestPlace")
    mock_dependencies["place_manager_factory"].create_place_manager.assert_called_once()
    place_manager.get_current_place_type.assert_called_once()
    place_manager.is_visited.assert_called_once_with("TestPlace")
    mock_dependencies["process_first_visit_factory"].create_command.assert_not_called()
    mock_dependencies[
        "config_loader"
    ].get_time_advanced_due_to_exiting_location.assert_called_once()
    mock_dependencies["time_manager"].advance_time.assert_called_once_with(5)


def test_execute_with_default_dependencies():
    with patch(
        "src.movements.commands.visit_place_command.PlaythroughManager"
    ) as mock_playthrough_manager_cls, patch(
        "src.movements.commands.visit_place_command.TimeManager"
    ) as mock_time_manager_cls, patch(
        "src.movements.commands.visit_place_command.ConfigLoader"
    ) as mock_config_loader_cls, patch(
        "src.movements.commands.visit_place_command.PlaceManagerFactory"
    ) as mock_place_manager_factory_cls, patch(
        "src.movements.commands.visit_place_command.ProcessFirstVisitToPlaceCommandFactory"
    ) as mock_process_first_visit_factory_cls:

        mock_playthrough_manager = Mock(spec=PlaythroughManager)
        mock_time_manager = Mock(spec=TimeManager)
        mock_config_loader = Mock(spec=ConfigLoader)
        mock_place_manager_factory = Mock(spec=PlaceManagerFactory)
        mock_process_first_visit_factory = Mock(
            spec=ProcessFirstVisitToPlaceCommandFactory
        )

        mock_playthrough_manager_cls.return_value = mock_playthrough_manager
        mock_time_manager_cls.return_value = mock_time_manager
        mock_config_loader_cls.return_value = mock_config_loader
        mock_place_manager_factory_cls.return_value = mock_place_manager_factory
        mock_process_first_visit_factory_cls.return_value = (
            mock_process_first_visit_factory
        )

        # Setup place manager behavior
        place_manager = Mock()
        place_manager.get_current_place_type.return_value = TemplateType.REGION
        place_manager.is_visited.return_value = False
        mock_place_manager_factory.create_place_manager.return_value = place_manager

        # Setup config loader
        mock_config_loader.get_time_advanced_due_to_exiting_location.return_value = 20

        # Setup first visit command
        first_visit_command = Mock(spec=Command)
        mock_process_first_visit_factory.create_command.return_value = (
            first_visit_command
        )

        cmd = VisitPlaceCommand(
            playthrough_name="DefaultPlaythrough",
            place_identifier="DefaultPlace",
            process_first_visit_to_place_command_factory=mock_process_first_visit_factory,
            place_manager_factory=mock_place_manager_factory,
        )

        # Act
        cmd.execute()

        # Assert
        mock_playthrough_manager.update_current_place.assert_called_once_with(
            "DefaultPlace"
        )
        mock_place_manager_factory.create_place_manager.assert_called_once()
        place_manager.get_current_place_type.assert_called_once()
        place_manager.is_visited.assert_called_once_with("DefaultPlace")
        mock_process_first_visit_factory.create_command.assert_called_once_with(
            "DefaultPlace"
        )
        first_visit_command.execute.assert_called_once()
        mock_config_loader.get_time_advanced_due_to_exiting_location.assert_called_once()
        mock_time_manager.advance_time.assert_called_once_with(20)


def test_execute_with_room_type_no_time_advance(mock_dependencies):
    # Arrange
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.ROOM

    mock_dependencies["place_manager_factory"].create_place_manager.return_value = (
        place_manager
    )

    cmd = VisitPlaceCommand(
        playthrough_name="TestPlaythrough",
        place_identifier="TestRoom",
        process_first_visit_to_place_command_factory=mock_dependencies[
            "process_first_visit_factory"
        ],
        place_manager_factory=mock_dependencies["place_manager_factory"],
        playthrough_manager=mock_dependencies["playthrough_manager"],
        time_manager=mock_dependencies["time_manager"],
        config_loader=mock_dependencies["config_loader"],
    )

    # Act
    cmd.execute()

    # Assert
    mock_dependencies[
        "playthrough_manager"
    ].update_current_place.assert_called_once_with("TestRoom")
    mock_dependencies["place_manager_factory"].create_place_manager.assert_called_once()
    place_manager.get_current_place_type.assert_called_once()
    place_manager.is_visited.assert_not_called()
    mock_dependencies["process_first_visit_factory"].create_command.assert_not_called()
    mock_dependencies[
        "config_loader"
    ].get_time_advanced_due_to_exiting_location.assert_not_called()
    mock_dependencies["time_manager"].advance_time.assert_not_called()


def test_execute_advance_time_called_correctly(mock_dependencies):
    # Arrange
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager.is_visited.return_value = True

    mock_dependencies["place_manager_factory"].create_place_manager.return_value = (
        place_manager
    )
    mock_dependencies[
        "config_loader"
    ].get_time_advanced_due_to_exiting_location.return_value = 15

    cmd = VisitPlaceCommand(
        playthrough_name="TestPlaythrough",
        place_identifier="TestLocation",
        process_first_visit_to_place_command_factory=mock_dependencies[
            "process_first_visit_factory"
        ],
        place_manager_factory=mock_dependencies["place_manager_factory"],
        playthrough_manager=mock_dependencies["playthrough_manager"],
        time_manager=mock_dependencies["time_manager"],
        config_loader=mock_dependencies["config_loader"],
    )

    # Act
    cmd.execute()

    # Assert
    mock_dependencies["time_manager"].advance_time.assert_called_once_with(15)
