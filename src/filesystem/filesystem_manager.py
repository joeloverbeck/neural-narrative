import json
import os
import sys

from src.constants import CHARACTERS_FOLDER_NAME, PLAYTHROUGHS_FOLDER, CHARACTERS_FILE, \
    SECRET_KEY_FILE, PLAYTHROUGH_METADATA_FILE, MEMORIES_FILE, DIALOGUES_FILE, WORLD_TEMPLATES_FILE, \
    LOCATIONS_TEMPLATES_FILE, MAP_FILE, AREAS_TEMPLATES_FILE, REGIONS_TEMPLATES_FILE


class FilesystemManager:
    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()

    @staticmethod
    def read_json_file(file_path: str) -> dict:
        """Load JSON data from a file."""
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def write_file(file_path, contents: str):
        with open(file_path, "a") as file:
            file.write(contents)

    @staticmethod
    def save_json_file(json_data, file_path):
        # Write the updated data back to the file
        with open(file_path, "w") as f:
            json.dump(json_data, f, indent=4)

    @staticmethod
    def load_existing_or_new_json_file(file_path: str):
        """
        Load existing data from a JSON file or create a new file if it doesn't exist.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The contents of the JSON file, either loaded or initialized as an empty dictionary.
        """
        if not file_path:
            raise ValueError("Attempted to load or create new JSON file, but the path wasn't valid.")

        # If the file doesn't exist, create it and write an empty dictionary to it
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump({}, f)

        # Load the existing data from the file
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def does_file_path_exist(file_path):
        return os.path.exists(file_path)

    def load_secret_key(self):
        try:
            # Attempt to load the secret key
            return self.read_file(SECRET_KEY_FILE)
        except FileNotFoundError:
            sys.exit(f"Error: File '{SECRET_KEY_FILE}'not found. Please check the file path.")
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def get_file_path_to_playthroughs_folder():
        # Ensure the playthroughs folder exists
        if not os.path.exists(PLAYTHROUGHS_FOLDER):
            os.makedirs(PLAYTHROUGHS_FOLDER)

        return PLAYTHROUGHS_FOLDER

    @staticmethod
    def create_folders_along_file_path(file_path):
        os.makedirs(file_path)

    def get_file_path_to_playthrough_folder(self, playthrough_name: str):
        return os.path.join(self.get_file_path_to_playthroughs_folder(), playthrough_name)

    @staticmethod
    def get_file_path_to_worlds_template_file():
        return WORLD_TEMPLATES_FILE

    @staticmethod
    def get_file_path_to_locations_template_file():
        return LOCATIONS_TEMPLATES_FILE

    @staticmethod
    def get_file_path_to_areas_template_file():
        return AREAS_TEMPLATES_FILE

    @staticmethod
    def get_file_path_to_regions_template_file():
        return REGIONS_TEMPLATES_FILE

    def get_file_path_to_playthrough_metadata(self, playthrough_name: str):
        return os.path.join(self.get_file_path_to_playthrough_folder(playthrough_name), PLAYTHROUGH_METADATA_FILE)

    def get_file_path_to_map(self, playthrough_name: str):
        return os.path.join(self.get_file_path_to_playthrough_folder(playthrough_name), MAP_FILE)

    def get_file_path_to_characters(self, playthrough_name: str):
        return os.path.join(self.get_file_path_to_playthroughs_folder(), playthrough_name, CHARACTERS_FOLDER_NAME)

    def get_file_path_to_characters_file(self, playthrough_name: str):
        # Build the path to the characters folder
        characters_folder = self.get_file_path_to_characters(playthrough_name)
        os.makedirs(characters_folder, exist_ok=True)

        # Build the path to the characters.json file
        return os.path.join(characters_folder, CHARACTERS_FILE)

    def get_file_path_to_character_folder(self, playthrough_name: str, character_identifier: int, character_data: dict):
        folder_name = f"{character_data['name']} - {character_identifier}"
        file_path = os.path.join(self.get_file_path_to_characters(playthrough_name), folder_name)

        # Create the folder if it doesn't exist
        os.makedirs(file_path, exist_ok=True)

        return file_path

    def get_file_path_to_character_dialogues(self, playthrough_name: str, character_identifier: int,
                                             character_data: dict):
        # Define the path
        folder_path = self.get_file_path_to_character_folder(playthrough_name, character_identifier, character_data)

        # Define the path to the "dialogues.txt" file
        return os.path.join(folder_path, DIALOGUES_FILE)

    def get_file_path_to_character_memories(self, playthrough_name: str, character_identifier: int,
                                            character_data: dict):
        # Define the path to the "memories.txt" file
        return os.path.join(
            self.get_file_path_to_character_folder(playthrough_name, character_identifier, character_data),
            MEMORIES_FILE)
