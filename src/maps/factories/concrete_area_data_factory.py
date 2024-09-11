from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import AreaDataFactory
from src.maps.abstracts.factory_products import AreaDataProduct
from src.maps.products.concrete_area_data_product import ConcreteAreaDataProduct


class ConcreteAreaDataFactory(AreaDataFactory):
    def __init__(self, playthrough_name: str, place_identifier: str):
        assert playthrough_name
        assert place_identifier

        self._playthrough_name = playthrough_name
        self._area_identifier = place_identifier

    def create_area_data(self) -> AreaDataProduct:
        filesystem_manager = FilesystemManager()

        # We have the area identifier, so we must load the map
        map_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_map(self._playthrough_name))

        corresponding_place = map_file[self._area_identifier]

        if corresponding_place["type"] != "area":
            return ConcreteAreaDataProduct({}, is_valid=False,
                                           error=f"The place provided doesn't correspond to an area: {corresponding_place}")

        # The corresponding place is indeed an area
        areas = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_areas_template_file())

        corresponding_area = areas[corresponding_place["place_template"]]

        return ConcreteAreaDataProduct(
            {"name": corresponding_place["place_template"], "description": corresponding_area["description"]},
            is_valid=True)
