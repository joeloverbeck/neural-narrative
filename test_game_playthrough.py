import os

import pytest

from game_playthrough import create_game_playthrough_folder


@pytest.fixture
def cleanup():
    """Cleanup any folders created during the test."""
    yield
    if os.path.exists("TestPlaythrough"):
        os.rmdir("TestPlaythrough")


def test_create_folder_when_not_exists(cleanup):
    # Setup
    playthrough_name = "TestPlaythrough"

    # Act
    create_game_playthrough_folder(playthrough_name)

    # Assert
    assert os.path.exists(playthrough_name), "Folder should be created when it doesn't exist"


def test_no_action_when_folder_exists(cleanup):
    # Setup
    playthrough_name = "TestPlaythrough"
    os.mkdir(playthrough_name)

    # Act
    create_game_playthrough_folder(playthrough_name)

    # Assert
    assert os.path.exists(playthrough_name), "Folder should still exist after function call"
    assert len(os.listdir(playthrough_name)) == 0, "Folder contents should not be altered"
