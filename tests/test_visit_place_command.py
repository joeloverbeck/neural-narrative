# test_visit_place_command.py
from unittest.mock import Mock

from src.base.required_string import RequiredString
from src.movements.commands.visit_place_command import VisitPlaceCommand

# Assuming the following constant is defined somewhere in your codebase
TIME_ADVANCED_DUE_TO_EXITING_LOCATION = 10  # Example value


# Mock implementations for the dependencies
# Since these are imported from src.*, we need to create mocks for them.
class Command:
    pass


class PlaythroughManager:
    def __init__(self, playthrough_name):
        pass

    def update_current_place(self, place_identifier: str):
        pass

    def get_story_universe_template(self) -> str:
        pass


class TimeManager:
    def __init__(self, playthrough_name):
        pass

    def advance_time(self, time_unit: int):
        pass


class CharacterGuidelinesManager:
    def guidelines_exist(
        self,
        story_universe_name: str,
        world_template: str,
        region_template: str,
        area_template: str,
        location_template: str,
    ) -> bool:
        pass


class GenerateCharacterGenerationGuidelinesAlgorithm:
    def do_algorithm(self):
        pass


class GenerateCharacterGenerationGuidelinesAlgorithmFactory:
    def create_algorithm(self) -> GenerateCharacterGenerationGuidelinesAlgorithm:
        pass


class HierarchyManager:
    def fill_places_templates_parameter(self, place_identifier):
        pass


class HierarchyManagerFactory:
    def create_hierarchy_manager(self) -> HierarchyManager:
        pass


class PlaceManager:
    def is_visited(self, place_identifier) -> bool:
        pass

    def set_as_visited(self, place_identifier):
        pass


class PlaceManagerFactory:
    def create_place_manager(self) -> PlaceManager:
        pass


def test_execute_updates_current_place():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    place_identifier = RequiredString("test_place")

    # Create mocks
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    playthrough_manager_mock.update_current_place = Mock()

    place_manager_mock = Mock(spec=PlaceManager)
    place_manager_mock.is_visited.return_value = True  # Assume place is visited

    place_manager_factory_mock = Mock(spec=PlaceManagerFactory)
    place_manager_factory_mock.create_place_manager.return_value = place_manager_mock

    time_manager_mock = Mock(spec=TimeManager)
    time_manager_mock.advance_time = Mock()

    # Instantiate the command with mocks
    command = VisitPlaceCommand(
        playthrough_name=playthrough_name,
        place_identifier=place_identifier,
        generate_character_generation_guidelines_algorithm_factory=Mock(
            spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory
        ),
        hierarchy_manager_factory=Mock(spec=HierarchyManagerFactory),
        place_manager_factory=place_manager_factory_mock,
        playthrough_manager=playthrough_manager_mock,
        time_manager=time_manager_mock,
        character_guidelines_manager=Mock(spec=CharacterGuidelinesManager),
    )

    # Act
    command.execute()

    # Assert
    playthrough_manager_mock.update_current_place.assert_called_once_with(
        place_identifier
    )


def test_execute_handles_new_place_guidelines_do_not_exist():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    place_identifier = RequiredString("new_place")

    # Mock playthrough manager
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    playthrough_manager_mock.update_current_place = Mock()
    playthrough_manager_mock.get_story_universe_template.return_value = "test_universe"

    # Mock place manager to return that the place has not been visited
    place_manager_mock = Mock(spec=PlaceManager)
    place_manager_mock.is_visited.return_value = False  # Place is not visited

    place_manager_factory_mock = Mock(spec=PlaceManagerFactory)
    place_manager_factory_mock.create_place_manager.return_value = place_manager_mock

    # Mock time manager
    time_manager_mock = Mock(spec=TimeManager)
    time_manager_mock.advance_time = Mock()

    # Mock character guidelines manager to return that guidelines do not exist
    character_guidelines_manager_mock = Mock(spec=CharacterGuidelinesManager)
    character_guidelines_manager_mock.guidelines_exist.return_value = (
        False  # Guidelines do not exist
    )

    # Mock generate algorithm
    generate_algorithm_mock = Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithm)
    generate_algorithm_mock.do_algorithm = Mock()

    generate_character_guidelines_algorithm_factory_mock = Mock(
        spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory
    )
    generate_character_guidelines_algorithm_factory_mock.create_algorithm.return_value = (
        generate_algorithm_mock
    )

    # Mock hierarchy manager
    hierarchy_manager_mock = Mock(spec=HierarchyManager)
    hierarchy_manager_mock.fill_places_templates_parameter.return_value = Mock(
        get_world_template=lambda: "world_template",
        get_region_template=lambda: "region_template",
        get_area_template=lambda: "area_template",
        get_location_template=lambda: "location_template",
    )

    hierarchy_manager_factory_mock = Mock(spec=HierarchyManagerFactory)
    hierarchy_manager_factory_mock.create_hierarchy_manager.return_value = (
        hierarchy_manager_mock
    )

    # Instantiate the command with mocks
    command = VisitPlaceCommand(
        playthrough_name=playthrough_name,
        place_identifier=place_identifier,
        generate_character_generation_guidelines_algorithm_factory=generate_character_guidelines_algorithm_factory_mock,
        hierarchy_manager_factory=hierarchy_manager_factory_mock,
        place_manager_factory=place_manager_factory_mock,
        playthrough_manager=playthrough_manager_mock,
        time_manager=time_manager_mock,
        character_guidelines_manager=character_guidelines_manager_mock,
    )

    # Act
    command.execute()

    # Assert
    playthrough_manager_mock.update_current_place.assert_called_once_with(
        place_identifier
    )
    place_manager_mock.is_visited.assert_called_once_with(place_identifier)
    character_guidelines_manager_mock.guidelines_exist.assert_called_once_with(
        "test_universe",
        "world_template",
        "region_template",
        "area_template",
        "location_template",
    )
    generate_algorithm_mock.do_algorithm.assert_called_once()
    place_manager_mock.set_as_visited.assert_called_once_with(place_identifier)


def test_execute_handles_new_place_guidelines_exist():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    place_identifier = RequiredString("new_place")

    # Mock playthrough manager
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    playthrough_manager_mock.update_current_place = Mock()
    playthrough_manager_mock.get_story_universe_template.return_value = "test_universe"

    # Mock place manager to return that the place has not been visited
    place_manager_mock = Mock(spec=PlaceManager)
    place_manager_mock.is_visited.return_value = False  # Place is not visited

    place_manager_factory_mock = Mock(spec=PlaceManagerFactory)
    place_manager_factory_mock.create_place_manager.return_value = place_manager_mock

    # Mock time manager
    time_manager_mock = Mock(spec=TimeManager)
    time_manager_mock.advance_time = Mock()

    # Mock character guidelines manager to return that guidelines exist
    character_guidelines_manager_mock = Mock(spec=CharacterGuidelinesManager)
    character_guidelines_manager_mock.guidelines_exist.return_value = (
        True  # Guidelines exist
    )

    # Mock generate algorithm
    generate_algorithm_mock = Mock(spec=GenerateCharacterGenerationGuidelinesAlgorithm)
    generate_algorithm_mock.do_algorithm = Mock()

    generate_character_guidelines_algorithm_factory_mock = Mock(
        spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory
    )
    generate_character_guidelines_algorithm_factory_mock.create_algorithm.return_value = (
        generate_algorithm_mock
    )

    # Mock hierarchy manager
    hierarchy_manager_mock = Mock(spec=HierarchyManager)
    hierarchy_manager_mock.fill_places_templates_parameter.return_value = Mock(
        get_world_template=lambda: "world_template",
        get_region_template=lambda: "region_template",
        get_area_template=lambda: "area_template",
        get_location_template=lambda: "location_template",
    )

    hierarchy_manager_factory_mock = Mock(spec=HierarchyManagerFactory)
    hierarchy_manager_factory_mock.create_hierarchy_manager.return_value = (
        hierarchy_manager_mock
    )

    # Instantiate the command with mocks
    command = VisitPlaceCommand(
        playthrough_name=playthrough_name,
        place_identifier=place_identifier,
        generate_character_generation_guidelines_algorithm_factory=generate_character_guidelines_algorithm_factory_mock,
        hierarchy_manager_factory=hierarchy_manager_factory_mock,
        place_manager_factory=place_manager_factory_mock,
        playthrough_manager=playthrough_manager_mock,
        time_manager=time_manager_mock,
        character_guidelines_manager=character_guidelines_manager_mock,
    )

    # Act
    command.execute()

    # Assert
    playthrough_manager_mock.update_current_place.assert_called_once_with(
        place_identifier
    )
    place_manager_mock.is_visited.assert_called_once_with(place_identifier)
    character_guidelines_manager_mock.guidelines_exist.assert_called_once_with(
        "test_universe",
        "world_template",
        "region_template",
        "area_template",
        "location_template",
    )
    generate_algorithm_mock.do_algorithm.assert_not_called()
    place_manager_mock.set_as_visited.assert_called_once_with(place_identifier)


def test_execute_place_already_visited():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    place_identifier = RequiredString("visited_place")

    # Mock playthrough manager
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    playthrough_manager_mock.update_current_place = Mock()

    # Mock place manager to return that the place has been visited
    place_manager_mock = Mock(spec=PlaceManager)
    place_manager_mock.is_visited.return_value = True  # Place is visited

    place_manager_factory_mock = Mock(spec=PlaceManagerFactory)
    place_manager_factory_mock.create_place_manager.return_value = place_manager_mock

    # Mock time manager
    time_manager_mock = Mock(spec=TimeManager)
    time_manager_mock.advance_time = Mock()

    # Mock character guidelines manager
    character_guidelines_manager_mock = Mock(spec=CharacterGuidelinesManager)
    character_guidelines_manager_mock.guidelines_exist = Mock()

    # Mock generate algorithm factory
    generate_character_guidelines_algorithm_factory_mock = Mock(
        spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory
    )
    generate_character_guidelines_algorithm_factory_mock.create_algorithm = Mock()

    # Instantiate the command with mocks
    command = VisitPlaceCommand(
        playthrough_name=playthrough_name,
        place_identifier=place_identifier,
        generate_character_generation_guidelines_algorithm_factory=generate_character_guidelines_algorithm_factory_mock,
        hierarchy_manager_factory=Mock(spec=HierarchyManagerFactory),
        place_manager_factory=place_manager_factory_mock,
        playthrough_manager=playthrough_manager_mock,
        time_manager=time_manager_mock,
        character_guidelines_manager=character_guidelines_manager_mock,
    )

    # Act
    command.execute()

    # Assert
    playthrough_manager_mock.update_current_place.assert_called_once_with(
        place_identifier
    )
    place_manager_mock.is_visited.assert_called_once_with(place_identifier)
    character_guidelines_manager_mock.guidelines_exist.assert_not_called()
    generate_character_guidelines_algorithm_factory_mock.create_algorithm.assert_not_called()


def test_multiple_visits_do_not_regenerate_guidelines():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    place_identifier = RequiredString("revisited_place")

    # Mock playthrough manager
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    playthrough_manager_mock.update_current_place = Mock()

    # Mock place manager to return that the place has been visited
    place_manager_mock = Mock(spec=PlaceManager)
    place_manager_mock.is_visited.return_value = True  # Place is visited

    place_manager_factory_mock = Mock(spec=PlaceManagerFactory)
    place_manager_factory_mock.create_place_manager.return_value = place_manager_mock

    # Mock time manager
    time_manager_mock = Mock(spec=TimeManager)
    time_manager_mock.advance_time = Mock()

    # Mock character guidelines manager
    character_guidelines_manager_mock = Mock(spec=CharacterGuidelinesManager)

    # Mock generate algorithm factory
    generate_character_guidelines_algorithm_factory_mock = Mock(
        spec=GenerateCharacterGenerationGuidelinesAlgorithmFactory
    )

    # Instantiate the command with mocks
    command = VisitPlaceCommand(
        playthrough_name=playthrough_name,
        place_identifier=place_identifier,
        generate_character_generation_guidelines_algorithm_factory=generate_character_guidelines_algorithm_factory_mock,
        hierarchy_manager_factory=Mock(spec=HierarchyManagerFactory),
        place_manager_factory=place_manager_factory_mock,
        playthrough_manager=playthrough_manager_mock,
        time_manager=time_manager_mock,
        character_guidelines_manager=character_guidelines_manager_mock,
    )

    # Act
    command.execute()
    command.execute()  # Execute a second time

    # Assert
    playthrough_manager_mock.update_current_place.assert_called_with(place_identifier)
    assert playthrough_manager_mock.update_current_place.call_count == 2
    generate_character_guidelines_algorithm_factory_mock.create_algorithm.assert_not_called()
