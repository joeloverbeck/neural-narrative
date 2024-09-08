import os

from src.filesystem.filesystem_manager import FilesystemManager


def load_character_data(playthrough_name: str, character_identifier: int):
    filesystem_manager = FilesystemManager()

    # Define the path
    file_path = filesystem_manager.get_file_path_to_characters_file(playthrough_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")

    # Load the JSON data from the file
    characters_data = filesystem_manager.read_json_file(file_path)

    # Return the character data for the given identifier
    if str(character_identifier) not in characters_data:
        raise KeyError(f"Character with identifier '{character_identifier}' not found.")

    return characters_data[str(character_identifier)]


def load_character_memories(playthrough_name: str, character_identifier: int):
    filesystem_manager = FilesystemManager()

    character_data = load_character_data(playthrough_name, character_identifier)

    file_path = filesystem_manager.get_file_path_to_character_memories(playthrough_name, character_identifier,
                                                                       character_data)

    # Check if the file exists, and if not, create an empty file
    if not os.path.exists(file_path):
        # Create an empty file
        with open(file_path, 'w') as f:
            pass  # This will create the empty file

    return filesystem_manager.read_file(file_path)
