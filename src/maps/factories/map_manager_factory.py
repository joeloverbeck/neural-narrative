from src.maps.map_manager import MapManager
from src.maps.map_repository import MapRepository
from src.maps.place_manager import PlaceManager


class MapManagerFactory:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def create_map_manager(self) -> MapManager:
        map_repository = MapRepository(self._playthrough_name)
        place_manager = PlaceManager(self._playthrough_name, map_repository)

        return MapManager(self._playthrough_name, place_manager, map_repository)
