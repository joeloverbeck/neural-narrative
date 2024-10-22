from src.maps.map_repository import MapRepository
from src.maps.place_manager import PlaceManager
from src.maps.templates_repository import TemplatesRepository


class PlaceManagerFactory:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def create_place_manager(self) -> PlaceManager:
        map_repository = MapRepository(self._playthrough_name)
        return PlaceManager(self._playthrough_name, map_repository,
                            TemplatesRepository())
