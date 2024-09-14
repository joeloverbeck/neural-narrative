from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import CurrentPlaceFactory
from src.maps.abstracts.factory_products import CurrentPlaceProduct
from src.maps.map_manager import MapManager
from src.maps.products.concrete_current_place_product import ConcreteCurrentPlaceProduct


class ConcreteCurrentPlaceFactory(CurrentPlaceFactory):
    def __init__(self, playthrough_name: str, map_manager: MapManager = None):
        assert playthrough_name

        self._playthrough_name = playthrough_name
        self._map_manager = map_manager or MapManager(playthrough_name)

    def create_current_place(self) -> CurrentPlaceProduct:
        filesystem_manager = FilesystemManager()

        map_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_map(self._playthrough_name))

        return ConcreteCurrentPlaceProduct(
            map_file[self._map_manager.get_current_place_identifier(self._playthrough_name)],
            is_valid=True)
