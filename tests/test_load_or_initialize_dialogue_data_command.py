# tests/test_load_or_initialize_dialogue_data_command.py

from unittest.mock import create_autospec, patch

import pytest

# Import the necessary classes and interfaces
from src.base.abstracts.command import Command
from src.dialogues.abstracts.strategies import ChooseParticipantsStrategy
from src.dialogues.commands.load_or_initialize_dialogue_data_command import (
    LoadOrInitializeDialogueDataCommand,
)
from src.dialogues.dialogue_manager import DialogueManager
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import (
    LoadDataFromOngoingDialogueCommandFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)
from src.dialogues.transcription import Transcription


# Assuming the LoadOrInitializeDialogueDataCommand is in src.commands.load_or_initialize_dialogue_data_command


@pytest.fixture
def mock_load_data_factory():
    return create_autospec(LoadDataFromOngoingDialogueCommandFactory)


@pytest.fixture
def mock_choose_participants_strategy():
    return create_autospec(ChooseParticipantsStrategy)


@pytest.fixture
def mock_dialogue_manager():
    return create_autospec(DialogueManager)


@pytest.fixture
def mock_ongoing_dialogue_repository():
    return create_autospec(OngoingDialogueRepository)


@pytest.fixture
def transcription():
    return create_autospec(Transcription)


@pytest.fixture
def participants():
    return Participants()


@pytest.fixture
def player_identifier():
    return "player_1"


@pytest.fixture
def playthrough_name():
    return "test_playthrough"


def test_constructor_validates_non_empty_strings():
    with pytest.raises(ValueError):
        LoadOrInitializeDialogueDataCommand(
            playthrough_name="",
            player_identifier="valid_player",
            participants=create_autospec(Participants),
            transcription=create_autospec(Transcription),
            load_data_from_ongoing_dialogue_command_factory=create_autospec(
                LoadDataFromOngoingDialogueCommandFactory
            ),
            choose_participants_strategy=create_autospec(ChooseParticipantsStrategy),
        )

    with pytest.raises(ValueError):
        LoadOrInitializeDialogueDataCommand(
            playthrough_name="valid_playthrough",
            player_identifier="",
            participants=create_autospec(Participants),
            transcription=create_autospec(Transcription),
            load_data_from_ongoing_dialogue_command_factory=create_autospec(
                LoadDataFromOngoingDialogueCommandFactory
            ),
            choose_participants_strategy=create_autospec(ChooseParticipantsStrategy),
        )


def test_execute_loads_existing_dialogue_data_when_participants_exist(
    mock_load_data_factory,
    mock_ongoing_dialogue_repository,
    transcription,
    participants,
    player_identifier,
    playthrough_name,
):
    # Arrange
    mock_ongoing_dialogue_repository.has_participants.return_value = True

    command = LoadOrInitializeDialogueDataCommand(
        playthrough_name=playthrough_name,
        player_identifier=player_identifier,
        participants=participants,
        transcription=transcription,
        load_data_from_ongoing_dialogue_command_factory=mock_load_data_factory,
        choose_participants_strategy=create_autospec(ChooseParticipantsStrategy),
        ongoing_dialogue_repository=mock_ongoing_dialogue_repository,
    )

    mock_load_command = create_autospec(Command)
    mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.return_value = (
        mock_load_command
    )

    # Act
    command.execute()

    # Assert
    mock_ongoing_dialogue_repository.has_participants.assert_called_once()
    mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.assert_called_once_with(
        transcription
    )
    mock_load_command.execute.assert_called_once()


def test_execute_initializes_new_dialogue_data_when_no_participants_exist(
    mock_load_data_factory,
    mock_choose_participants_strategy,
    mock_dialogue_manager,
    mock_ongoing_dialogue_repository,
    transcription,
    participants,
    player_identifier,
    playthrough_name,
):
    # Arrange
    mock_ongoing_dialogue_repository.has_participants.return_value = False
    mock_choose_participants_strategy.choose_participants.return_value = [
        "participant_1",
        "participant_2",
    ]

    command = LoadOrInitializeDialogueDataCommand(
        playthrough_name=playthrough_name,
        player_identifier=player_identifier,
        participants=participants,
        transcription=transcription,
        load_data_from_ongoing_dialogue_command_factory=mock_load_data_factory,
        choose_participants_strategy=mock_choose_participants_strategy,
        dialogue_manager=mock_dialogue_manager,
        ongoing_dialogue_repository=mock_ongoing_dialogue_repository,
    )

    # Act
    command.execute()

    # Assert
    mock_ongoing_dialogue_repository.has_participants.assert_called_once()
    mock_choose_participants_strategy.choose_participants.assert_called_once()
    mock_dialogue_manager.gather_participants_data.assert_called_once_with(
        player_identifier, ["participant_1", "participant_2"], participants
    )
    # Ensure that load_data_from_ongoing_dialogue_command_factory.create_load_data_from_ongoing_dialogue_command is not called
    mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.assert_not_called()


def test_execute_initializes_new_dialogue_with_default_dialogue_manager_and_repository(
    mock_load_data_factory,
    mock_choose_participants_strategy,
    mock_ongoing_dialogue_repository,
    transcription,
    participants,
    player_identifier,
    playthrough_name,
):
    # Arrange
    mock_ongoing_dialogue_repository.has_participants.return_value = False
    mock_choose_participants_strategy.choose_participants.return_value = [
        "participant_1",
        "participant_2",
    ]

    with patch(
        "src.dialogues.commands.load_or_initialize_dialogue_data_command.DialogueManager"
    ) as MockDialogueManager, patch(
        "src.dialogues.commands.load_or_initialize_dialogue_data_command.OngoingDialogueRepository"
    ) as MockOngoingDialogueRepository:

        mock_dialogue_manager = create_autospec(DialogueManager)
        MockDialogueManager.return_value = mock_dialogue_manager  # noqa

        mock_ongoing_repo = create_autospec(OngoingDialogueRepository)
        MockOngoingDialogueRepository.return_value = mock_ongoing_repo

        command = LoadOrInitializeDialogueDataCommand(
            playthrough_name=playthrough_name,
            player_identifier=player_identifier,
            participants=participants,
            transcription=transcription,
            load_data_from_ongoing_dialogue_command_factory=mock_load_data_factory,
            choose_participants_strategy=mock_choose_participants_strategy,
            # Not providing dialogue_manager and ongoing_dialogue_repository
        )

        # Override the has_participants method to return False
        mock_ongoing_repo.has_participants.return_value = False

        # Act
        command.execute()

        # Assert
        MockDialogueManager.assert_called_once_with(playthrough_name)
        MockOngoingDialogueRepository.assert_called_once_with(playthrough_name)
        mock_choose_participants_strategy.choose_participants.assert_called_once()
        mock_dialogue_manager.gather_participants_data.assert_called_once_with(  # noqa
            player_identifier, ["participant_1", "participant_2"], participants
        )
        mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.assert_not_called()


def test_execute_loads_data_when_has_participants_and_default_repository(
    mock_load_data_factory,
    transcription,
    participants,
    player_identifier,
    playthrough_name,
):
    # Arrange
    with patch(
        "src.dialogues.commands.load_or_initialize_dialogue_data_command.OngoingDialogueRepository"
    ) as MockOngoingDialogueRepository:
        mock_ongoing_repo = create_autospec(OngoingDialogueRepository)
        mock_ongoing_repo.has_participants.return_value = True
        MockOngoingDialogueRepository.return_value = mock_ongoing_repo

        command = LoadOrInitializeDialogueDataCommand(
            playthrough_name=playthrough_name,
            player_identifier=player_identifier,
            participants=participants,
            transcription=transcription,
            load_data_from_ongoing_dialogue_command_factory=mock_load_data_factory,
            choose_participants_strategy=create_autospec(ChooseParticipantsStrategy),
            # Not providing dialogue_manager and ongoing_dialogue_repository
        )

        mock_load_command = create_autospec(Command)
        mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.return_value = (
            mock_load_command
        )

        # Act
        command.execute()

        # Assert
        MockOngoingDialogueRepository.assert_called_once_with(playthrough_name)
        mock_ongoing_repo.has_participants.assert_called_once()
        mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.assert_called_once_with(
            transcription
        )
        mock_load_command.execute.assert_called_once()


def test_execute_raises_exception_when_factory_fails(
    mock_load_data_factory,
    mock_ongoing_dialogue_repository,
    transcription,
    participants,
    player_identifier,
    playthrough_name,
):
    # Arrange
    mock_ongoing_dialogue_repository.has_participants.return_value = True
    mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.side_effect = Exception(
        "Factory failure"
    )

    command = LoadOrInitializeDialogueDataCommand(
        playthrough_name=playthrough_name,
        player_identifier=player_identifier,
        participants=participants,
        transcription=transcription,
        load_data_from_ongoing_dialogue_command_factory=mock_load_data_factory,
        choose_participants_strategy=create_autospec(ChooseParticipantsStrategy),
        ongoing_dialogue_repository=mock_ongoing_dialogue_repository,
    )

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        command.execute()

    assert "Factory failure" in str(exc_info.value)
    mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.assert_called_once_with(
        transcription
    )
    # Ensure that execute was not called since factory failed
    # (No load_command was created due to exception)


def test_execute_raises_exception_when_choose_participants_fails(
    mock_choose_participants_strategy,
    mock_dialogue_manager,
    mock_load_data_factory,
    mock_ongoing_dialogue_repository,
    transcription,
    participants,
    player_identifier,
    playthrough_name,
):
    # Arrange
    mock_ongoing_dialogue_repository.has_participants.return_value = False
    mock_choose_participants_strategy.choose_participants.side_effect = Exception(
        "Choose participants failure"
    )

    command = LoadOrInitializeDialogueDataCommand(
        playthrough_name=playthrough_name,
        player_identifier=player_identifier,
        participants=participants,
        transcription=transcription,
        load_data_from_ongoing_dialogue_command_factory=mock_load_data_factory,
        choose_participants_strategy=mock_choose_participants_strategy,
        dialogue_manager=mock_dialogue_manager,
        ongoing_dialogue_repository=mock_ongoing_dialogue_repository,
    )

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        command.execute()

    assert "Choose participants failure" in str(exc_info.value)
    mock_choose_participants_strategy.choose_participants.assert_called_once()
    mock_dialogue_manager.gather_participants_data.assert_not_called()
    mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.assert_not_called()


def test_execute_does_not_initialize_dialogue_if_participants_already_exist(
    mock_load_data_factory,
    mock_ongoing_dialogue_repository,
    transcription,
    participants,
    player_identifier,
    playthrough_name,
):
    # Arrange
    mock_ongoing_dialogue_repository.has_participants.return_value = True

    command = LoadOrInitializeDialogueDataCommand(
        playthrough_name=playthrough_name,
        player_identifier=player_identifier,
        participants=participants,
        transcription=transcription,
        load_data_from_ongoing_dialogue_command_factory=mock_load_data_factory,
        choose_participants_strategy=create_autospec(ChooseParticipantsStrategy),
        ongoing_dialogue_repository=mock_ongoing_dialogue_repository,
    )

    mock_load_command = create_autospec(Command)
    mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.return_value = (
        mock_load_command
    )

    # Act
    command.execute()

    # Assert
    mock_ongoing_dialogue_repository.has_participants.assert_called_once()
    mock_load_data_factory.create_load_data_from_ongoing_dialogue_command.assert_called_once_with(
        transcription
    )
    mock_load_command.execute.assert_called_once()


def test_execute_initializes_dialogue_with_correct_parameters(
    mock_choose_participants_strategy,
    mock_dialogue_manager,
    mock_load_data_factory,
    mock_ongoing_dialogue_repository,
    transcription,
    participants,
    player_identifier,
    playthrough_name,
):
    # Arrange
    mock_ongoing_dialogue_repository.has_participants.return_value = False
    chosen_participants = ["participant_A", "participant_B", "participant_C"]
    mock_choose_participants_strategy.choose_participants.return_value = (
        chosen_participants
    )

    command = LoadOrInitializeDialogueDataCommand(
        playthrough_name=playthrough_name,
        player_identifier=player_identifier,
        participants=participants,
        transcription=transcription,
        load_data_from_ongoing_dialogue_command_factory=mock_load_data_factory,
        choose_participants_strategy=mock_choose_participants_strategy,
        dialogue_manager=mock_dialogue_manager,
        ongoing_dialogue_repository=mock_ongoing_dialogue_repository,
    )

    # Act
    command.execute()

    # Assert
    mock_choose_participants_strategy.choose_participants.assert_called_once()
    mock_dialogue_manager.gather_participants_data.assert_called_once_with(
        player_identifier, chosen_participants, participants
    )
