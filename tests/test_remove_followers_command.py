from unittest.mock import patch, Mock, call

import pytest

from src.base.commands.remove_followers_command import RemoveFollowersCommand
from src.base.playthrough_manager import PlaythroughManager
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


def test_remove_followers_command_init_valid():
    playthrough_name = "TestPlaythrough"
    follower_identifiers = ["follower1", "follower2"]
    place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )

    command = RemoveFollowersCommand(
        playthrough_name, follower_identifiers, place_character_at_place_command_factory
    )

    assert command._playthrough_manager is not None
    assert command._follower_identifiers == follower_identifiers
    assert (
        command._place_character_at_place_command_factory
        == place_character_at_place_command_factory
    )


def test_remove_followers_command_init_empty_playthrough_name():
    playthrough_name = ""
    follower_identifiers = ["follower1", "follower2"]
    place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )

    with pytest.raises(ValueError) as exc_info:
        RemoveFollowersCommand(
            playthrough_name,
            follower_identifiers,
            place_character_at_place_command_factory,
        )
    assert "'playthrough_name' must be a non-empty string." in str(exc_info.value)


def test_remove_followers_command_init_none_playthrough_name():
    playthrough_name = None
    follower_identifiers = ["follower1", "follower2"]
    place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )

    with pytest.raises(ValueError) as exc_info:
        RemoveFollowersCommand(
            playthrough_name,  # noqa
            follower_identifiers,
            place_character_at_place_command_factory,
        )
    assert "'playthrough_name' must be a non-empty string." in str(exc_info.value)


def test_remove_followers_command_init_whitespace_playthrough_name():
    playthrough_name = "   "
    follower_identifiers = ["follower1", "follower2"]
    place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )

    with pytest.raises(ValueError) as exc_info:
        RemoveFollowersCommand(
            playthrough_name,
            follower_identifiers,
            place_character_at_place_command_factory,
        )
    assert "'playthrough_name' must be a non-empty string." in str(exc_info.value)


def test_remove_followers_command_execute():
    playthrough_name = "TestPlaythrough"
    follower_identifiers = ["follower1", "follower2"]

    mock_playthrough_manager = Mock(spec=PlaythroughManager)
    current_place_identifier = "current_place"
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    mock_place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )
    mock_commands = [Mock(), Mock()]
    mock_place_character_at_place_command_factory.create_command.side_effect = (
        mock_commands
    )

    command = RemoveFollowersCommand(
        playthrough_name,
        follower_identifiers,
        mock_place_character_at_place_command_factory,
        playthrough_manager=mock_playthrough_manager,
    )
    command.execute()

    expected_calls_remove_follower = [
        call(follower_id) for follower_id in follower_identifiers
    ]
    assert (
        mock_playthrough_manager.remove_follower.call_args_list
        == expected_calls_remove_follower
    )

    expected_calls_create_command = [
        call(follower_id, current_place_identifier)
        for follower_id in follower_identifiers
    ]
    assert (
        mock_place_character_at_place_command_factory.create_command.call_args_list
        == expected_calls_create_command
    )

    for mock_command in mock_commands:
        mock_command.execute.assert_called_once()


def test_remove_followers_command_execute_empty_followers():
    playthrough_name = "TestPlaythrough"
    follower_identifiers = []

    mock_playthrough_manager = Mock(spec=PlaythroughManager)
    current_place_identifier = "current_place"
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    mock_place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )

    command = RemoveFollowersCommand(
        playthrough_name,
        follower_identifiers,
        mock_place_character_at_place_command_factory,
        playthrough_manager=mock_playthrough_manager,
    )
    command.execute()

    mock_playthrough_manager.remove_follower.assert_not_called()
    mock_place_character_at_place_command_factory.create_command.assert_not_called()


def test_remove_followers_command_execute_none_follower_identifiers():
    playthrough_name = "TestPlaythrough"
    follower_identifiers = None
    place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )

    with pytest.raises(TypeError) as exc_info:
        RemoveFollowersCommand(
            playthrough_name,
            follower_identifiers,  # noqa
            place_character_at_place_command_factory,
        )

    assert "The passed value is not a list: <class 'NoneType'>" in str(exc_info.value)


def test_remove_followers_command_execute_invalid_follower_identifiers():
    playthrough_name = "TestPlaythrough"
    follower_identifiers = ["follower1", 123, None]

    mock_playthrough_manager = Mock(spec=PlaythroughManager)
    current_place_identifier = "current_place"
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    mock_place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )
    mock_commands = [Mock(), Mock(), Mock()]
    mock_place_character_at_place_command_factory.create_command.side_effect = (
        mock_commands
    )

    with pytest.raises(Exception):
        RemoveFollowersCommand(
            playthrough_name,
            follower_identifiers,
            mock_place_character_at_place_command_factory,
            playthrough_manager=mock_playthrough_manager,
        )


def test_remove_followers_command_init_creates_playthrough_manager():
    playthrough_name = "TestPlaythrough"
    follower_identifiers = ["follower1", "follower2"]
    place_character_at_place_command_factory = Mock(
        spec=PlaceCharacterAtPlaceCommandFactory
    )

    with patch(
        "src.base.commands.remove_followers_command.PlaythroughManager"
    ) as MockPlaythroughManager:
        command = RemoveFollowersCommand(
            playthrough_name,
            follower_identifiers,
            place_character_at_place_command_factory,
        )
        MockPlaythroughManager.assert_called_once_with(playthrough_name)
        assert command._playthrough_manager == MockPlaythroughManager.return_value
