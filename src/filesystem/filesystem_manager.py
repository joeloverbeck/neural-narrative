import json
import os
import sys
from datetime import datetime
from typing import List, Any

from src.constants import (
    CHARACTERS_FOLDER_NAME,
    PLAYTHROUGHS_FOLDER,
    CHARACTERS_FILE,
    OPENROUTER_SECRET_KEY_FILE,
    PLAYTHROUGH_METADATA_FILE,
    MEMORIES_FILE,
    DIALOGUES_FILE,
    MAP_FILE,
    LOGGING_CONFIG_FILE,
    OPENAI_SECRET_KEY_FILE,
    IMAGES_FOLDER_NAME,
    OPENAI_PROJECT_KEY_FILE,
    ONGOING_DIALOGUE_FOLDER_NAME,
    RUNPOD_SECRET_KEY_FILE,
)


class FilesystemManager:
    @staticmethod
    def read_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    def read_file_lines(self, file_path) -> List[str]:
        if os.path.exists(file_path):
            concepts_content = self.read_file(file_path)
            return concepts_content.strip().split("\n") if concepts_content else []
        else:
            return []

    @staticmethod
    def read_json_file(file_path: str) -> dict:
        """Load JSON data from a file."""
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def create_empty_file_if_not_exists(file_path: str) -> None:
        """Create an empty file if it does not exist."""
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                pass  # This will create an empty file

    @staticmethod
    def append_to_file(file_path: str, contents: str) -> None:
        """Append the given contents to the file."""
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(contents)

    @staticmethod
    def write_file(file_path: str, contents: str) -> None:
        """Write contents to a file, overwriting any existing data."""
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(contents)

    @staticmethod
    def write_binary_file(file_path: str, contents: bytes) -> None:
        """Write binary contents to a file."""
        with open(file_path, "wb") as f:
            f.write(contents)

    @staticmethod
    def save_json_file(json_data: Any, file_path: str) -> None:
        """Serialize json_data to a JSON-formatted file with proper encoding."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

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
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

        # Load the existing data from the file
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def remove_item_from_file(file_path, index):
        """Remove a line at a specific index from a file."""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                lines = [line.rstrip("\n") for line in file if line.strip()]
            if 0 <= index < len(lines):
                del lines[index]
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("\n".join(lines))

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

    def load_runpod_secret_key(self) -> str:
        try:
            # Attempt to load the secret key
            return self.read_file(RUNPOD_SECRET_KEY_FILE)
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{RUNPOD_SECRET_KEY_FILE}'not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def get_file_path_for_voice_line(
        character_name: str, voice_model: str
    ) -> (str, str):
        if not character_name:
            raise ValueError("character_name can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")

        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Generate a unique filename to prevent overwriting
        file_name = f"{timestamp}-{character_name}-{voice_model}.wav"

        folder_path = "static/voice_lines"

        # Ensure the 'voice_lines' directory exists
        os.makedirs(folder_path, exist_ok=True)

        return file_name, os.path.join(folder_path, file_name)

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

    def get_file_path_to_interesting_dilemmas(self, playthrough_name: str) -> str:
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            "interesting_dilemmas.txt",
        )

    def get_file_path_to_goals(self, playthrough_name: str) -> str:
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name), "goals.txt"
        )

    @staticmethod
    def get_file_path_to_empty_content_context_file() -> str:
        file_path = "errors/empty_content_context.txt"

        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        return file_path

    def remove_ongoing_dialogue(self, playthrough_name: str):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        file_path = self.get_file_path_to_ongoing_dialogue(playthrough_name)

        if os.path.exists(file_path):
            os.remove(file_path)

    def get_file_path_to_playthrough_metadata(self, playthrough_name: str):
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            PLAYTHROUGH_METADATA_FILE,
        )

    def get_file_path_to_adventure(self, playthrough_name: str):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            "adventure.txt",
        )

    def get_file_path_to_concepts(self, playthrough_name: str):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name), "concepts.txt"
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
