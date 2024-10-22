from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_descriptions_for_prompt_factory import PlaceDescriptionsForPromptFactory
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.maps.weathers_manager import WeathersManager


class PlacesDescriptionsProviderComposer:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def compose_provider(self) -> PlacesDescriptionsProvider:
        map_manager_factory = MapManagerFactory(self._playthrough_name)
        weathers_manager = WeathersManager(map_manager_factory)
        place_descriptions_for_prompt_factory = (
            PlaceDescriptionsForPromptFactory(self._playthrough_name,
                                              map_manager_factory, weathers_manager))
        return PlacesDescriptionsProvider(place_descriptions_for_prompt_factory
                                          )
