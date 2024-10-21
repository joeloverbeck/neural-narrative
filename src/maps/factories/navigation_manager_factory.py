from src.maps.map_repository import MapRepository
from src.maps.navigation_manager import NavigationManager


class NavigationManagerFactory:
    def __init__(self, map_repository: MapRepository):
        self._map_repository = map_repository

    def create_navigation_manager(self) -> NavigationManager:
        return NavigationManager(self._map_repository)
