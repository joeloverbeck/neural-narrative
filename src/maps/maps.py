from src.filesystem.filesystem_manager import FilesystemManager


def is_current_place_a_location(playthrough_name: str) -> bool:
    assert playthrough_name

    filesystem_manager = FilesystemManager()

    playthrough_metadata = filesystem_manager.load_existing_or_new_json_file(
        filesystem_manager.get_file_path_to_playthrough_metadata(playthrough_name))

    map_file = filesystem_manager.load_existing_or_new_json_file(
        filesystem_manager.get_file_path_to_map(playthrough_name))

    current_place = map_file[playthrough_metadata["current_place"]]

    return current_place["type"] == "location"
