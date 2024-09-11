from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import CurrentLocationDataFactory
from src.maps.abstracts.factory_products import CurrentLocationDataProduct
from src.maps.products.concrete_current_location_data_product import ConcreteCurrentLocationDataProduct


class ConcreteCurrentLocationDataFactory(CurrentLocationDataFactory):
    def __init__(self, playthrough_name: str):
        assert playthrough_name

        self._playthrough_name = playthrough_name

    def create_current_location_data(self) -> CurrentLocationDataProduct:
        # First, load the playthrough metadata to find out the current place.
        filesystem_manager = FilesystemManager()

        playthrough_metadata = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        # Now that we have the playthrough metadata, we need to load the map.
        map_json = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_map(self._playthrough_name))

        current_place = map_json[playthrough_metadata["current_place"]]

        # We have now the current place as located in the map. It will have a type, and according
        # to that we will be able to know if it's a location or an area.

        # Given that this class only retrieves locations, if the type isn't a location,
        # then the caller did something wrong.
        if current_place["type"] != "location":
            return ConcreteCurrentLocationDataProduct({}, is_valid=False,
                                                      error=f"The current place isn't a location. It was '{current_place["type"]}'.")

        # After this point, the current place is a location.
        # We should retrieve the "locations" json
        locations = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_locations_template_file())

        # fill the data and return it.
        return ConcreteCurrentLocationDataProduct(
            {"name": current_place["place_template"],
             "description": locations[current_place["place_template"]]["description"],
             "area": current_place["area"]},
            is_valid=True)
