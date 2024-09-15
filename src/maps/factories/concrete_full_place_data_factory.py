from src.maps.abstracts.factory_products import FullPlaceDataProduct
from src.maps.map_manager import MapManager
from src.maps.products.concrete_ful_place_data_product import ConcreteFullPlaceDataProduct


class ConcreteFullPlaceDataFactory:

    def __init__(self, playthrough_name: str, map_manager: MapManager = None):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        self._playthrough_name = playthrough_name

        self._map_manager = map_manager or MapManager(self._playthrough_name)

    def create_full_place_data(self) -> FullPlaceDataProduct:
        return ConcreteFullPlaceDataProduct(self._map_manager.get_place_full_data(
            self._map_manager.get_current_place_identifier(self._playthrough_name)), is_valid=True)
