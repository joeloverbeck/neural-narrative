from src.base.required_string import RequiredString
from src.maps.map_manager import MapManager
from src.maps.map_repository import MapRepository
from src.maps.place_manager import PlaceManager
from src.maps.templates_repository import TemplatesRepository


class MapManagerFactory:
    def __init__(self, playthrough_name: RequiredString):
        self._playthrough_name = playthrough_name

    def create_map_manager(self) -> MapManager:
        map_repository = MapRepository(self._playthrough_name)

        template_repository = TemplatesRepository()

        place_manager = PlaceManager(
            self._playthrough_name, map_repository, template_repository
        )

        return MapManager(
            self._playthrough_name, place_manager, map_repository, template_repository
        )
