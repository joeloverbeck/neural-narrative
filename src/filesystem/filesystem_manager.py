import json
import os
import sys
from typing import List

from src.constants import (
    CHARACTERS_FOLDER_NAME,
    PLAYTHROUGHS_FOLDER,
    CHARACTERS_FILE,
    OPENROUTER_SECRET_KEY_FILE,
    PLAYTHROUGH_METADATA_FILE,
    MEMORIES_FILE,
    DIALOGUES_FILE,
    WORLD_TEMPLATES_FILE,
    LOCATIONS_TEMPLATES_FILE,
    MAP_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
    LOGGING_CONFIG_FILE,
    OPENAI_SECRET_KEY_FILE,
    IMAGES_FOLDER_NAME,
    OPENAI_PROJECT_KEY_FILE,
    ONGOING_DIALOGUE_FOLDER_NAME,
    CONFIG_FILE,
    CHARACTER_GENERATION_GUIDELINES_FILE,
)


class FilesystemManager:
    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()

    @staticmethod
    def read_json_file(file_path: str) -> dict:
        """Load JSON data from a file."""
        with open(file_path, "r") as file:
            return json.load(file)

    @staticmethod
    def create_empty_file_if_not_exists(file_path: str):
        if not os.path.exists(file_path):
            # Create an empty file
            with open(file_path, "w") as f:
                pass  # This will create the empty file

    @staticmethod
    def append_to_file(file_path, contents: str):
        with open(file_path, "a") as file:
            file.write(contents)

    @staticmethod
    def write_file(file_path, contents: str):
        """This function removes the previous contents of the file."""
        with open(file_path, "w") as file:
            file.write(contents)

    @staticmethod
    def write_binary_file(file_path, contents: bytes):
        with open(file_path, "wb") as f:
            f.write(contents)

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
            raise ValueError(
                "Attempted to load or create new JSON file, but the path wasn't valid."
            )

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

    def load_openrouter_secret_key(self):
        try:
            # Attempt to load the secret key
            return self.read_file(OPENROUTER_SECRET_KEY_FILE)
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENROUTER_SECRET_KEY_FILE}'not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    def load_openai_secret_key(self):
        try:
            # Attempt to load the secret key
            return self.read_file(OPENAI_SECRET_KEY_FILE)
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENAI_SECRET_KEY_FILE}' not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    def load_openai_project_key(self):
        try:
            # Attempt to load the secret key
            return self.read_file(OPENAI_PROJECT_KEY_FILE)
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENAI_PROJECT_KEY_FILE}' not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def get_file_path_to_config_file():
        return CONFIG_FILE

    @staticmethod
    def get_file_path_to_playthroughs_folder():
        # Ensure the playthroughs folder exists
        if not os.path.exists(PLAYTHROUGHS_FOLDER):
            os.makedirs(PLAYTHROUGHS_FOLDER)

        return PLAYTHROUGHS_FOLDER

    def get_playthrough_names(self) -> List[str]:
        playthroughs_folder = self.get_file_path_to_playthroughs_folder()

        # Retrieve the list of existing playthrough folders
        if os.path.exists(playthroughs_folder):
            return [
                name
                for name in os.listdir(playthroughs_folder)
                if os.path.isdir(os.path.join(playthroughs_folder, name))
            ]
        else:
            return []

    def playthrough_exists(self, playthrough_name):
        return playthrough_name in self.get_playthrough_names()

    @staticmethod
    def create_folders_along_file_path(file_path):
        os.makedirs(file_path)

    def get_file_path_to_playthrough_folder(self, playthrough_name: str):
        return os.path.join(
            self.get_file_path_to_playthroughs_folder(), playthrough_name
        )

    def get_file_path_to_ongoing_dialogue(self, playthrough_name) -> str:
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            ONGOING_DIALOGUE_FOLDER_NAME,
        )

    def get_file_path_to_ongoing_dialogue_folder(self, playthrough_name: str) -> str:
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        folder_path = self.get_file_path_to_ongoing_dialogue(playthrough_name)

        if not folder_path:
            os.makedirs(folder_path)

        return folder_path

    def get_file_path_to_interesting_situations(self, playthrough_name: str) -> str:
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            "interesting_situations.txt",
        )

    @staticmethod
    def get_file_path_to_empty_content_context_file() -> str:
        errors_folder = "errors"

        if not errors_folder:
            os.makedirs(errors_folder)

        return os.path.join(errors_folder, "empty_content_context.json")

    def remove_ongoing_dialogue(self, playthrough_name: str):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        file_path = self.get_file_path_to_ongoing_dialogue(playthrough_name)

        if os.path.exists(file_path):
            os.remove(file_path)

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
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            PLAYTHROUGH_METADATA_FILE,
        )

    def get_file_path_to_map(self, playthrough_name: str):
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name), MAP_FILE
        )

    def get_file_path_to_characters(self, playthrough_name: str):
        return os.path.join(
            self.get_file_path_to_playthroughs_folder(),
            playthrough_name,
            CHARACTERS_FOLDER_NAME,
        )

    @staticmethod
    def get_file_path_to_character_generation_guidelines_file():
        return CHARACTER_GENERATION_GUIDELINES_FILE

    @staticmethod
    def get_file_path_to_character_images(playthrough_name: str) -> str:
        images_path = os.path.join(
            f"static/{PLAYTHROUGHS_FOLDER}/{playthrough_name}", IMAGES_FOLDER_NAME
        )
        os.makedirs(images_path, exist_ok=True)

        return images_path

    def get_file_path_to_character_image(
        self, playthrough_name: str, character_identifier: str
    ):
        return os.path.join(
            self.get_file_path_to_character_images(playthrough_name),
            f"{character_identifier}.png",
        )

    @staticmethod
    def get_file_path_to_character_image_for_web(
        playthrough_name: str, character_identifier: str
    ):
        return f"playthroughs/{playthrough_name}/{IMAGES_FOLDER_NAME}/{character_identifier}.png"

    def get_file_path_to_characters_file(self, playthrough_name: str):
        # Build the path to the characters folder
        characters_folder = self.get_file_path_to_characters(playthrough_name)
        os.makedirs(characters_folder, exist_ok=True)

        # Build the path to the characters.json file
        return os.path.join(characters_folder, CHARACTERS_FILE)

    def get_file_path_to_character_folder(
        self, playthrough_name: str, character_identifier: str, character_name: str
    ):
        folder_name = f"{character_name} - {character_identifier}"
        file_path = os.path.join(
            self.get_file_path_to_characters(playthrough_name), folder_name
        )

        # Create the folder if it doesn't exist
        os.makedirs(file_path, exist_ok=True)

        return file_path

    def get_file_path_to_character_dialogues(
        self, playthrough_name: str, character_identifier: str, character_name: str
    ):
        if not isinstance(character_name, str):
            raise TypeError(
                f"character_name should have been a string, but was '{type(character_name)}'"
            )

        # Define the path
        folder_path = self.get_file_path_to_character_folder(
            playthrough_name, character_identifier, character_name
        )

        # Define the path to the "dialogues.txt" file
        return os.path.join(folder_path, DIALOGUES_FILE)

    def get_file_path_to_character_memories(
        self, playthrough_name: str, character_identifier: str, character_name: str
    ):
        if not isinstance(character_name, str):
            raise TypeError(
                f"character_name should have been a string, but was '{type(character_name)}'"
            )

        # Define the path to the "memories.txt" file
        return os.path.join(
            self.get_file_path_to_character_folder(
                playthrough_name, character_identifier, character_name
            ),
            MEMORIES_FILE,
        )

    def get_logging_config_file(self) -> dict:
        return self.load_existing_or_new_json_file(LOGGING_CONFIG_FILE)
