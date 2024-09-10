import json
import sys

from src.filesystem.filesystem_manager import FilesystemManager


def determine_next_identifier(playthrough_name: str, identifier_type):
    # Join the folder and file to get the full path
    filesystem_manager = FilesystemManager()

    file_path = filesystem_manager.get_file_path_to_playthrough_metadata(playthrough_name)

    # Load the JSON file
    with open(file_path, "r") as f:
        playthrough_metadata = json.load(f)

    current_value = -1

    # Get the value based on the identifier type
    try:
        current_value = int(playthrough_metadata["last_identifiers"][identifier_type.value])
    except KeyError as error:
        print(f"Key error: {error}")
        sys.exit()

    # Increment the value by 1
    return current_value + 1
