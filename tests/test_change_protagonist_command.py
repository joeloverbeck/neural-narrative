from unittest.mock import MagicMock, patch

import pytest

from src.base.commands.change_protagonist_command import ChangeProtagonistCommand
from src.base.configs.change_protagonist_command_config import (
    ChangeProtagonistCommandConfig,
)
from src.base.configs.change_protagonist_command_factories_config import (
    ChangeProtagonistCommandFactoriesConfig,
)
from src.base.factories.remove_followers_command_factory import (
    RemoveFollowersCommandFactory,
)
from src.base.playthrough_manager import PlaythroughManager
from src.maps.factories.get_place_identifier_of_character_location_algorithm_factory import (
    GetPlaceIdentifierOfCharacterLocationAlgorithmFactory,
)
from src.maps.factories.remove_character_from_place_command_factory import (
    RemoveCharacterFromPlaceCommandFactory,
)
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


@pytest.fixture
def setup_dependencies():
    # Mock the factories
    place_character_factory = MagicMock(spec=PlaceCharacterAtPlaceCommandFactory)
    remove_followers_factory = MagicMock(spec=RemoveFollowersCommandFactory)
    get_place_algorithm_factory = MagicMock(
        spec=GetPlaceIdentifierOfCharacterLocationAlgorithmFactory
    )
    remove_character_factory = MagicMock(spec=RemoveCharacterFromPlaceCommandFactory)

    factories_config = ChangeProtagonistCommandFactoriesConfig(
        place_character_at_place_command_factory=place_character_factory,
        remove_followers_command_factory=remove_followers_factory,
        get_place_identifier_of_character_location_algorithm_factory=get_place_algorithm_factory,
        remove_character_from_place_command_factory=remove_character_factory,
    )

    # Mock the playthrough manager
    playthrough_manager = MagicMock(spec=PlaythroughManager)
    playthrough_manager.get_player_identifier.return_value = "current_protagonist"
    playthrough_manager.get_current_place_identifier.return_value = "current_place"
    playthrough_manager.get_followers.return_value = ["follower1", "follower2"]

    # Set up the config
    config = ChangeProtagonistCommandConfig(
        playthrough_name="test_playthrough",
        new_protagonist_identifier="new_protagonist",
    )

    return config, factories_config, playthrough_manager


def test_execute_updates_player_identifier(setup_dependencies):
    config, factories_config, playthrough_manager = setup_dependencies

    command = ChangeProtagonistCommand(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager,
    )

    command.execute()

    playthrough_manager.update_player_identifier.assert_called_once_with(
        config.new_protagonist_identifier
    )


def test_execute_places_current_protagonist(setup_dependencies):
    config, factories_config, playthrough_manager = setup_dependencies

    place_character_command = MagicMock()
    factories_config.place_character_at_place_command_factory.create_command.return_value = (
        place_character_command
    )

    command = ChangeProtagonistCommand(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager,
    )

    command.execute()

    factories_config.place_character_at_place_command_factory.create_command.assert_called_once_with(  # noqa
        "current_protagonist", "current_place"
    )
    place_character_command.execute.assert_called_once()


def test_execute_removes_followers(setup_dependencies):
    config, factories_config, playthrough_manager = setup_dependencies

    remove_followers_command = MagicMock()
    factories_config.remove_followers_command_factory.create_command.return_value = (
        remove_followers_command
    )

    command = ChangeProtagonistCommand(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager,
    )

    command.execute()

    factories_config.remove_followers_command_factory.create_command.assert_called_once_with(  # noqa
        ["follower1", "follower2"]
    )
    remove_followers_command.execute.assert_called_once()


def test_execute_updates_current_place(setup_dependencies):
    config, factories_config, playthrough_manager = setup_dependencies

    get_place_algorithm = MagicMock()
    get_place_algorithm.do_algorithm.return_value = "new_protagonist_place"
    factories_config.get_place_identifier_of_character_location_algorithm_factory.create_algorithm.return_value = (
        get_place_algorithm
    )

    remove_character_command = MagicMock()
    factories_config.remove_character_from_place_command_factory.create_command.return_value = (
        remove_character_command
    )

    command = ChangeProtagonistCommand(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager,
    )

    command.execute()

    factories_config.get_place_identifier_of_character_location_algorithm_factory.create_algorithm.assert_called_once_with(  # noqa
        "new_protagonist"
    )
    get_place_algorithm.do_algorithm.assert_called_once()

    factories_config.remove_character_from_place_command_factory.create_command.assert_called_once_with(  # noqa
        "new_protagonist", "new_protagonist_place"
    )
    remove_character_command.execute.assert_called_once()

    playthrough_manager.update_current_place.assert_called_once_with(
        "new_protagonist_place"
    )


def test_execute_with_no_followers(setup_dependencies):
    config, factories_config, playthrough_manager = setup_dependencies
    playthrough_manager.get_followers.return_value = []

    remove_followers_command = MagicMock()
    factories_config.remove_followers_command_factory.create_command.return_value = (
        remove_followers_command
    )

    command = ChangeProtagonistCommand(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager,
    )

    command.execute()

    factories_config.remove_followers_command_factory.create_command.assert_called_once_with(  # noqa
        []
    )
    remove_followers_command.execute.assert_called_once()


def test_execute_without_playthrough_manager():
    config = ChangeProtagonistCommandConfig(
        playthrough_name="test_playthrough",
        new_protagonist_identifier="new_protagonist",
    )

    factories_config = MagicMock(spec=ChangeProtagonistCommandFactoriesConfig)

    with patch(
        "src.base.commands.change_protagonist_command.PlaythroughManager"
    ) as MockPlaythroughManager:
        playthrough_manager_instance = MockPlaythroughManager.return_value

        command = ChangeProtagonistCommand(
            config=config, factories_config=factories_config, playthrough_manager=None
        )

        MockPlaythroughManager.assert_called_once_with("test_playthrough")
        assert command._playthrough_manager == playthrough_manager_instance


def test_execute_with_invalid_new_protagonist(setup_dependencies):
    config, factories_config, playthrough_manager = setup_dependencies

    get_place_algorithm = MagicMock()
    get_place_algorithm.do_algorithm.side_effect = Exception("Character not found")
    factories_config.get_place_identifier_of_character_location_algorithm_factory.create_algorithm.return_value = (
        get_place_algorithm
    )

    command = ChangeProtagonistCommand(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager,
    )

    with pytest.raises(Exception) as exc_info:
        command.execute()

    assert str(exc_info.value) == "Character not found"
