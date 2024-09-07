import json
import os
import sys

from src.constants import SECRET_KEY_FILE, PLAYTHROUGHS_FOLDER, CHARACTERS_FOLDER_NAME, CHARACTERS_FILE


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()


def write_file(file_path, contents: str):
    with open(file_path, "a") as file:
        file.write(contents)


def load_existing_or_new_json_file(file_path):
    """
    Load existing data from a JSON file or create a new file if it doesn't exist.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file, either loaded or initialized as an empty dictionary.
    """
    # If the file doesn't exist, create it and write an empty dictionary to it
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({}, f)

    # Load the existing data from the file
    with open(file_path, "r") as f:
        return json.load(f)


def read_json_file(file_path: str) -> dict:
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json_file(json_data, file_path):
    # Write the updated data back to the file
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)


def get_file_path_to_characters(playthrough_name: str):
    return os.path.join(PLAYTHROUGHS_FOLDER, playthrough_name, CHARACTERS_FOLDER_NAME)


def get_file_path_to_character_folder(playthrough_name: str, character_identifier: int, character_data: dict):
    folder_name = f"{character_data['name']} - {character_identifier}"
    return os.path.join(get_file_path_to_characters(playthrough_name), folder_name)


def get_file_path_to_character_dialogues(playthrough_name: str, character_identifier: int, character_data: dict):
    # Define the path
    folder_path = get_file_path_to_character_folder(playthrough_name, character_identifier, character_data)

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Define the path to the "dialogues.txt" file
    return os.path.join(folder_path, "dialogues.txt")


def get_file_path_to_character_memories(playthrough_name: str, character_identifier: int, character_data: dict):
    # Define the path
    folder_path = get_file_path_to_character_folder(playthrough_name, character_identifier, character_data)

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Define the path to the "memories.txt" file
    return os.path.join(folder_path, "memories.txt")


def get_file_path_to_characters_file(playthrough_name: str):
    # Build the path to the characters folder
    characters_folder = get_file_path_to_characters(playthrough_name)
    os.makedirs(characters_folder, exist_ok=True)

    # Build the path to the characters.json file
    return os.path.join(characters_folder, CHARACTERS_FILE)


def load_secret_key():
    try:
        # Attempt to load the secret key
        return read_file(SECRET_KEY_FILE)
    except FileNotFoundError:
        sys.exit(f"Error: File '{SECRET_KEY_FILE}'not found. Please check the file path.")
    except Exception as e:
        sys.exit(f"An unexpected error occurred: {str(e)}")
