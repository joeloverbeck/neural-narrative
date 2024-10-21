from src.base.required_string import RequiredString
from src.maps.hierarchy_manager import HierarchyManager

from src.maps.map_repository import MapRepository
from src.maps.place_manager import PlaceManager
from src.maps.templates_repository import TemplatesRepository


class HierarchyManagerFactory:
    def __init__(self, playthrough_name: RequiredString):
        self._playthrough_name = playthrough_name

    def create_hierarchy_manager(self) -> HierarchyManager:
        map_repository = MapRepository(self._playthrough_name)

        place_manager = PlaceManager(
            self._playthrough_name, map_repository, TemplatesRepository()
        )

        return HierarchyManager(place_manager)
