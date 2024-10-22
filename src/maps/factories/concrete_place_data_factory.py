from src.base.constants import LOCATIONS_TEMPLATES_FILE, AREAS_TEMPLATES_FILE, REGIONS_TEMPLATES_FILE, \
    WORLDS_TEMPLATES_FILE
from src.base.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import PlaceDataFactory
from src.maps.abstracts.factory_products import PlaceDataProduct
from src.maps.products.concrete_place_data_product import ConcretePlaceDataProduct


class ConcretePlaceDataFactory(PlaceDataFactory):

    def __init__(self, playthrough_name: str, place_identifier: str):
        self._playthrough_name = playthrough_name
        self._place_identifier = place_identifier

    def create_place_data(self) -> PlaceDataProduct:
        filesystem_manager = FilesystemManager()
        map_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_map(self._playthrough_name))
        corresponding_place = map_file[self._place_identifier]
        if corresponding_place['type'] == TemplateType.LOCATION:
            locations = filesystem_manager.load_existing_or_new_json_file(
                LOCATIONS_TEMPLATES_FILE)
            corresponding_location = locations[corresponding_place[
                'place_template']]
            return ConcretePlaceDataProduct({'name': corresponding_place[
                'place_template'], 'description': corresponding_location[
                'description'], 'area': corresponding_place['area']},
                                            is_valid=True)
        if corresponding_place['type'] == TemplateType.AREA:
            areas = filesystem_manager.load_existing_or_new_json_file(
                AREAS_TEMPLATES_FILE)
            corresponding_area = areas[corresponding_place['place_template']]
            return ConcretePlaceDataProduct({'name': corresponding_place[
                'place_template'], 'description': corresponding_area[
                'description'], 'region': corresponding_place['region']},
                                            is_valid=True)
        if corresponding_place['type'] == TemplateType.REGION:
            regions = filesystem_manager.load_existing_or_new_json_file(
                REGIONS_TEMPLATES_FILE)
            corresponding_region = regions[corresponding_place[
                'place_template']]
            return ConcretePlaceDataProduct({'name': corresponding_place[
                'place_template'], 'description': corresponding_region[
                'description']}, is_valid=True)
        if corresponding_place['type'] == TemplateType.WORLD:
            worlds = filesystem_manager.load_existing_or_new_json_file(
                WORLDS_TEMPLATES_FILE)
            corresponding_world = worlds[corresponding_place['place_template']]
            return ConcretePlaceDataProduct({'name': corresponding_place[
                'place_template'], 'description': corresponding_world[
                'description']}, is_valid=True)
        raise ValueError(
            f"""When attempting to return the data of a place, the algorithm determine that the corresponding date wasn't a location, an area, a region, nor a world. This should never have happened.
{corresponding_place}"""
        )
