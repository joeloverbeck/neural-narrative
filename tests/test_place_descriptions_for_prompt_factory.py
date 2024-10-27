from unittest.mock import Mock

import pytest

from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)


class PlaythroughManager:

    def __init__(self, _playthrough_name):
        pass

    def get_current_place_identifier(self):
        pass


class WeathersManager:

    def __init__(self, _playthrough_name):
        pass

    def get_current_weather_identifier(self):
        pass

    def get_weather_description(self, weather_identifier):
        pass


class MapManagerFactory:

    def create_map_manager(self):
        pass


class MapManager:

    def get_story_universe_description(self):
        pass

    def get_place_full_data(self, place_identifier):
        pass


def test_init_with_provided_managers():
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    weathers_manager_mock = Mock(spec=WeathersManager)
    playthrough_name = "TestPlaythrough"
    map_manager_factory_mock = Mock(spec=MapManagerFactory)
    factory = PlaceDescriptionsForPromptFactory(
        playthrough_name=playthrough_name,
        map_manager_factory=map_manager_factory_mock,
        playthrough_manager=playthrough_manager_mock,
        weathers_manager=weathers_manager_mock,
    )
    assert factory._playthrough_manager is playthrough_manager_mock
    assert factory._weathers_manager is weathers_manager_mock


def test_determine_location_description_with_description():
    place_full_data = {
        "location_data": {"description": "A beautiful place with stunning scenery"}
    }
    expected = "Location Description: A beautiful place with stunning scenery"
    result = PlaceDescriptionsForPromptFactory._determine_location_description(
        place_full_data
    )
    assert result == expected


def test_determine_location_description_missing_location_data():
    place_full_data = {}
    with pytest.raises(KeyError):
        PlaceDescriptionsForPromptFactory._determine_location_description(
            place_full_data
        )


def test_create_place_descriptions_for_prompt():
    playthrough_name = "TestPlaythrough"
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    weathers_manager_mock = Mock(spec=WeathersManager)
    map_manager_factory_mock = Mock(spec=MapManagerFactory)
    map_manager_mock = Mock()
    map_manager_factory_mock.create_map_manager.return_value = map_manager_mock
    map_manager_mock.get_story_universe_description.return_value = (
        "A vast and mysterious universe."
    )
    playthrough_manager_mock.get_current_place_identifier.return_value = "place123"
    place_full_data = {
        "world_data": {"description": "A big world."},
        "region_data": {"description": "A lush green region."},
        "area_data": {"description": "An area filled with ancient ruins."},
        "location_data": {"description": "A hidden cave behind the waterfall."},
    }
    map_manager_mock.get_place_full_data.return_value = place_full_data
    weathers_manager_mock.get_current_weather_identifier.return_value = "weather456"
    weathers_manager_mock.get_weather_description.return_value = (
        "A gentle rain falls softly."
    )
    factory = PlaceDescriptionsForPromptFactory(
        playthrough_name=playthrough_name,
        map_manager_factory=map_manager_factory_mock,
        playthrough_manager=playthrough_manager_mock,
        weathers_manager=weathers_manager_mock,
    )
    result = factory.create_place_descriptions_for_prompt()
    expected = {
        "story_universe_description": "A vast and mysterious universe.",
        "world_description": "A big world.",
        "region_description": "A lush green region.",
        "area_description": "An area filled with ancient ruins.",
        "weather": "A gentle rain falls softly.",
        "location_description": "Location Description: A hidden cave behind the waterfall.",
    }
    assert result == expected


def test_create_place_descriptions_for_prompt_missing_location_data():
    playthrough_name = "TestPlaythrough"
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    weathers_manager_mock = Mock(spec=WeathersManager)
    map_manager_factory_mock = Mock(spec=MapManagerFactory)
    map_manager_mock = Mock()
    map_manager_factory_mock.create_map_manager.return_value = map_manager_mock
    map_manager_mock.get_story_universe_description.return_value = (
        "A vast and mysterious universe."
    )
    playthrough_manager_mock.get_current_place_identifier.return_value = "place123"
    place_full_data = {
        "region_data": {"description": "A lush green region."},
        "area_data": {"description": "An area filled with ancient ruins."},
    }
    map_manager_mock.get_place_full_data.return_value = place_full_data
    weathers_manager_mock.get_current_weather_identifier.return_value = "weather456"
    weathers_manager_mock.get_weather_description.return_value = (
        "A gentle rain falls softly."
    )
    factory = PlaceDescriptionsForPromptFactory(
        playthrough_name=playthrough_name,
        map_manager_factory=map_manager_factory_mock,
        playthrough_manager=playthrough_manager_mock,
        weathers_manager=weathers_manager_mock,
    )
    with pytest.raises(KeyError):
        factory.create_place_descriptions_for_prompt()
