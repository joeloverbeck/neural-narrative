from src.enums import PlaceType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import CurrentPlaceFactory


def get_current_place_identifier(playthrough_name: str):
    assert playthrough_name

    filesystem_manager = FilesystemManager()

    playthrough_metadata = filesystem_manager.load_existing_or_new_json_file(
        filesystem_manager.get_file_path_to_playthrough_metadata(playthrough_name))

    return playthrough_metadata["current_place"]


def is_current_place_a_place_type(place_type: PlaceType, current_place_factory: CurrentPlaceFactory) -> bool:
    assert place_type
    assert current_place_factory

    current_place_product = current_place_factory.create_current_place()

    assert not isinstance(current_place_product, dict)

    if not current_place_product.is_valid():
        raise ValueError(f"Was unable to produce the current place data: {current_place_product.get_error()}")

    return current_place_product.get()["type"] == place_type.value
