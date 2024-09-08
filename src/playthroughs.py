from src.filesystem.filesystem_manager import FilesystemManager


def create_playthrough(playthrough_name, world_template: str):
    filesystem_manager = FilesystemManager()

    # Check if the folder already exists
    if filesystem_manager.does_file_path_exist(
            filesystem_manager.get_file_path_to_playthrough_folder(playthrough_name)):
        raise Exception(f"A playthrough with the name '{playthrough_name}' already exists.")

    # Checks here if there is such a world template:
    worlds_file = filesystem_manager.load_existing_or_new_json_file(
        filesystem_manager.get_file_path_to_worlds_template_file())

    if world_template not in worlds_file:
        raise ValueError(f"There is no such world template '{world_template}'")

    filesystem_manager.create_folders_along_file_path(
        filesystem_manager.get_file_path_to_playthrough_folder(playthrough_name))

    playthrough_metadata = {
        "world_template": world_template,
        "last_identifiers": {
            "places": "0",
            "characters": "0"
        }
    }

    # Write the initial values to the JSON file
    filesystem_manager.save_json_file(playthrough_metadata,
                                      filesystem_manager.get_file_path_to_playthrough_metadata(playthrough_name))

    return filesystem_manager.get_file_path_to_playthrough_folder(playthrough_name)
