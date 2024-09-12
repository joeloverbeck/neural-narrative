from src.enums import PlaceType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import PlaceDataFactory
from src.maps.abstracts.factory_products import PlaceDataProduct
from src.maps.products.concrete_place_data_product import ConcretePlaceDataProduct


class ConcretePlaceDataFactory(PlaceDataFactory):
    def __init__(self, playthrough_name: str, place_identifier: str):
        assert playthrough_name
        assert place_identifier

        self._playthrough_name = playthrough_name
        self._place_identifier = place_identifier

    def create_place_data(self) -> PlaceDataProduct:
        filesystem_manager = FilesystemManager()

        # We have the place identifier, so we must load the map
        map_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_map(self._playthrough_name))

        corresponding_place = map_file[self._place_identifier]

        # This place could be a location, an area, or a region.
        if corresponding_place["type"] == PlaceType.LOCATION.value:
            locations = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_locations_template_file())

            corresponding_location = locations[corresponding_place["place_template"]]

            return ConcretePlaceDataProduct(
                {"name": corresponding_place["place_template"], "description": corresponding_location["description"],
                 "area": corresponding_place["area"]},
                is_valid=True)

        if corresponding_place["type"] == PlaceType.AREA.value:
            areas = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_areas_template_file())

            corresponding_area = areas[corresponding_place["place_template"]]

            return ConcretePlaceDataProduct(
                {"name": corresponding_place["place_template"], "description": corresponding_area["description"],
                 "region": corresponding_place["region"]},
                is_valid=True)

        if corresponding_place["type"] == PlaceType.REGION.value:
            regions = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_regions_template_file())

            corresponding_region = regions[corresponding_place["place_template"]]

            return ConcretePlaceDataProduct({
                "name": corresponding_place["place_template"], "description": corresponding_region["description"]
            }, is_valid=True)

        raise ValueError(
            f"When attempting to return the data of a place, the algorithm determine that the corresponding date wasn't a location, an area, nor a region. This should never have happened.\n{corresponding_place}")
