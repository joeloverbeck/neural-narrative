from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.characters.factories.generate_character_generation_guidelines_algorithm_factory import (
    GenerateCharacterGenerationGuidelinesAlgorithmFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.commands.process_first_visit_to_place_command import (
    ProcessFirstVisitToPlaceCommand,
)


def test_execute_room_type_logs_warning_and_returns(caplog):
    # Set up mocks
    playthrough_name = "test_playthrough"
    map_entry_identifier = "test_map_entry"
    generate_factory = Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory)
    hierarchy_factory = Mock(spec=HierarchyManagerFactory)
    place_factory = Mock(spec=PlaceManagerFactory)
    playthrough_manager = Mock(spec=PlaythroughManager)
    character_manager = Mock(spec=CharacterGuidelinesManager)

    # Mock place_manager to return ROOM as current place type
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.ROOM
    place_factory.create_place_manager.return_value = place_manager

    # Instantiate the command
    command = ProcessFirstVisitToPlaceCommand(
        playthrough_name,
        map_entry_identifier,
        generate_factory,
        hierarchy_factory,
        place_factory,
        playthrough_manager,
        character_manager,
    )

    # Execute the command
    command.execute()

    # Check that a warning was logged
    assert "This command shouldn't be executed for rooms" in caplog.text

    # Ensure no further methods were called
    place_manager.set_as_visited.assert_not_called()
    generate_factory.create_algorithm.assert_not_called()


def test_execute_non_room_type_proceeds():
    # Set up mocks
    playthrough_name = "test_playthrough"
    map_entry_identifier = "test_map_entry"
    generate_factory = Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory)
    hierarchy_factory = Mock(spec=HierarchyManagerFactory)
    place_factory = Mock(spec=PlaceManagerFactory)
    playthrough_manager = Mock(spec=PlaythroughManager)
    character_manager = Mock(spec=CharacterGuidelinesManager)

    # Mock place_manager to return LOCATION as current place type
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_factory.create_place_manager.return_value = place_manager

    # Mock hierarchy_manager
    hierarchy_manager = Mock()
    hierarchy_factory.create_hierarchy_manager.return_value = hierarchy_manager

    # Mock places_templates_parameter
    places_templates_parameter = Mock()
    hierarchy_manager.fill_places_templates_parameter.return_value = (
        places_templates_parameter
    )

    # Mock character_manager
    character_manager.guidelines_exist.return_value = True

    # Instantiate the command
    command = ProcessFirstVisitToPlaceCommand(
        playthrough_name,
        map_entry_identifier,
        generate_factory,
        hierarchy_factory,
        place_factory,
        playthrough_manager,
        character_manager,
    )

    # Execute the command
    command.execute()

    # Check that place_manager.set_as_visited was called
    place_manager.set_as_visited.assert_called_once_with(map_entry_identifier)


def test_execute_guidelines_exist_do_not_generate():
    # Similar setup as previous test

    # Mock character_manager to return True
    character_manager = Mock(spec=CharacterGuidelinesManager)
    character_manager.guidelines_exist.return_value = True

    # Instantiate the command
    command = ProcessFirstVisitToPlaceCommand(
        "test_playthrough",
        "test_map_entry",
        Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory),
        Mock(spec=HierarchyManagerFactory),
        Mock(spec=PlaceManagerFactory),
        Mock(spec=PlaythroughManager),
        character_manager,
    )

    # Execute the command
    command.execute()

    # Check that generate_factory.create_algorithm().do_algorithm() was not called
    command._generate_character_generation_guidelines_algorithm_factory.create_algorithm.assert_not_called()


def test_execute_guidelines_do_not_exist_generate():
    # Set up mocks
    character_manager = Mock(spec=CharacterGuidelinesManager)
    character_manager.guidelines_exist.return_value = False

    generate_factory = Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory)
    algorithm = Mock()
    generate_factory.create_algorithm.return_value = algorithm

    # Instantiate the command
    command = ProcessFirstVisitToPlaceCommand(
        "test_playthrough",
        "test_map_entry",
        generate_factory,
        Mock(spec=HierarchyManagerFactory),
        Mock(spec=PlaceManagerFactory),
        Mock(spec=PlaythroughManager),
        character_manager,
    )

    # Execute the command
    command.execute()

    # Check that the algorithm's do_algorithm() wasn't called (config loader value would be null)
    algorithm.do_algorithm.assert_not_called()


def test_execute_sets_place_as_visited():
    # Set up mocks
    place_manager = Mock()
    place_factory = Mock(spec=PlaceManagerFactory)
    place_factory.create_place_manager.return_value = place_manager

    # Instantiate the command
    command = ProcessFirstVisitToPlaceCommand(
        "test_playthrough",
        "test_map_entry",
        Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory),
        Mock(spec=HierarchyManagerFactory),
        place_factory,
        Mock(spec=PlaythroughManager),
        Mock(spec=CharacterGuidelinesManager),
    )

    # Execute the command
    command.execute()

    # Check that set_as_visited was called with correct identifier
    place_manager.set_as_visited.assert_called_once_with("test_map_entry")


def test_init_with_empty_playthrough_name_raises_exception():
    with pytest.raises(ValueError) as excinfo:
        ProcessFirstVisitToPlaceCommand(
            "",
            "test_map_entry",
            Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory),
            Mock(spec=HierarchyManagerFactory),
            Mock(spec=PlaceManagerFactory),
        )
    assert "playthrough_name" in str(excinfo.value)


def test_init_with_empty_map_entry_identifier_raises_exception():
    with pytest.raises(ValueError) as excinfo:
        ProcessFirstVisitToPlaceCommand(
            "test_playthrough",
            "",
            Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory),
            Mock(spec=HierarchyManagerFactory),
            Mock(spec=PlaceManagerFactory),
        )
    assert "map_entry_identifier" in str(excinfo.value)


def test_execute_checks_guidelines_with_correct_parameters():
    # Set up mocks
    character_manager = Mock(spec=CharacterGuidelinesManager)
    character_manager.guidelines_exist.return_value = True

    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_story_universe_template.return_value = "story_universe"

    places_templates_parameter = Mock()
    places_templates_parameter.get_world_template.return_value = "world_template"
    places_templates_parameter.get_region_template.return_value = "region_template"
    places_templates_parameter.get_area_template.return_value = "area_template"
    places_templates_parameter.get_location_template.return_value = "location_template"

    hierarchy_manager = Mock()
    hierarchy_manager.fill_places_templates_parameter.return_value = (
        places_templates_parameter
    )

    hierarchy_factory = Mock(spec=HierarchyManagerFactory)
    hierarchy_factory.create_hierarchy_manager.return_value = hierarchy_manager

    # Instantiate the command
    command = ProcessFirstVisitToPlaceCommand(
        "test_playthrough",
        "test_map_entry",
        Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory),
        hierarchy_factory,
        Mock(spec=PlaceManagerFactory),
        playthrough_manager,
        character_manager,
    )

    # Execute the command
    command.execute()

    # Check that guidelines_exist was called with correct parameters
    character_manager.guidelines_exist.assert_called_once_with(
        "story_universe",
        "world_template",
        "region_template",
        "area_template",
        "location_template",
    )


def test_execute_calls_fill_places_templates_parameter_with_correct_argument():
    # Set up mocks
    hierarchy_manager = Mock()
    hierarchy_factory = Mock(spec=HierarchyManagerFactory)
    hierarchy_factory.create_hierarchy_manager.return_value = hierarchy_manager

    # Instantiate the command
    command = ProcessFirstVisitToPlaceCommand(
        "test_playthrough",
        "test_map_entry",
        Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory),
        hierarchy_factory,
        Mock(spec=PlaceManagerFactory),
        Mock(spec=PlaythroughManager),
    )

    # Execute the command
    command.execute()

    # Check that fill_places_templates_parameter was called with correct argument
    hierarchy_manager.fill_places_templates_parameter.assert_called_once_with(
        "test_map_entry"
    )


def test_execute_calls_get_story_universe_template():
    # Set up mocks
    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_story_universe_template.return_value = "story_universe"

    # Instantiate the command
    command = ProcessFirstVisitToPlaceCommand(
        "test_playthrough",
        "test_map_entry",
        Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory),
        Mock(spec=HierarchyManagerFactory),
        Mock(spec=PlaceManagerFactory),
        playthrough_manager,
    )

    # Execute the command
    command.execute()

    # Check that get_story_universe_template was called
    playthrough_manager.get_story_universe_template.assert_called_once()
