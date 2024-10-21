import json
import logging
import os
import sys
from datetime import datetime
from json import JSONDecodeError
from typing import List, Optional, Dict

from src.base.constants import (
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
    VOICE_LINES_FOLDER_PATH,
)
from src.base.exceptions import FailedToLoadJsonError
from src.base.required_string import RequiredString

logger = logging.getLogger(__name__)


class FilesystemManager:
    @staticmethod
    def read_file(file_path: RequiredString) -> Optional[RequiredString]:
        if not isinstance(file_path, RequiredString):
            file_path = RequiredString(file_path)

        with open(file_path.value, "r", encoding="utf-8") as file:
            file_contents = file.read().strip()

            if file_contents:
                return RequiredString(file_contents)

            return None

    def read_file_lines(self, file_path: RequiredString) -> List[RequiredString]:
        if not isinstance(file_path, RequiredString):
            file_path = RequiredString(file_path)

        if os.path.exists(file_path.value):
            file_content = self.read_file(file_path)
            return (
                [
                    RequiredString(line)
                    for line in file_content.value.strip().split("\n")
                    if line
                ]
                if file_content
                else []
            )

        else:
            return []

    @staticmethod
    def read_json_file(file_path: RequiredString) -> dict:
        """Load JSON data from a file."""
        with open(file_path.value, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def create_empty_file_if_not_exists(file_path: RequiredString) -> None:
        if not isinstance(file_path, RequiredString):
            file_path = RequiredString(file_path)

        """Create an empty file if it does not exist."""
        if not os.path.exists(file_path.value):
            with open(file_path.value, "w", encoding="utf-8"):
                pass  # This will create an empty file

    @staticmethod
    def append_to_file(file_path: RequiredString, contents: RequiredString) -> None:
        """Append the given contents to the file."""
        with open(file_path.value, "a", encoding="utf-8") as file:
            file.write(contents.value)

    @staticmethod
    def write_file(
            file_path: RequiredString, contents: Optional[RequiredString]
    ) -> None:
        """Write contents to a file, overwriting any existing data."""
        if not isinstance(file_path, RequiredString):
            file_path = RequiredString(file_path)

        with open(file_path.value, "w", encoding="utf-8") as file:
            if contents:
                # Could be that there are contents, but they aren't of type RequiredString
                if not isinstance(contents, RequiredString):
                    contents = RequiredString(contents)
                file.write(contents.value)
            else:
                file.write("")

    @staticmethod
    def write_binary_file(file_path: str, contents: bytes) -> None:
        """Write binary contents to a file."""
        with open(file_path, "wb") as f:
            f.write(contents)

    @staticmethod
    def save_json_file(json_data: Dict | List[Dict], file_path: RequiredString) -> None:
        """Serialize json_data to a JSON-formatted file with proper encoding."""
        with open(file_path.value, "w", encoding="utf-8") as f:
            logger.info("will attempt to save the following json data: %s", json_data)
            json.dump(json_data, f, indent=4, ensure_ascii=False)  # noqa: PyTypeChecker

    @staticmethod
    def load_existing_or_new_json_file(file_path: RequiredString) -> Dict:
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
        if not isinstance(file_path, RequiredString):
            file_path = RequiredString(file_path)

        # If the file doesn't exist, create it and write an empty dictionary to it
        if not os.path.exists(file_path.value):
            with open(
                    file_path.value, "w", encoding="utf-8"
            ) as f:  # noqa: PyTypeChecker
                json.dump({}, f)  # noqa: PyTypeChecker

        # Load the existing data from the file
        try:
            with open(file_path.value, "r", encoding="utf-8") as f:
                return json.load(f)
        except JSONDecodeError as e:
            raise FailedToLoadJsonError(
                f"Failed to load file '{file_path.value}'. Error: {e}"
            ) from e

    @staticmethod
    def remove_item_from_file(file_path: RequiredString, index: int):
        if not isinstance(file_path, RequiredString):
            file_path = RequiredString(file_path)

        """Remove a line at a specific index from a file."""
        if os.path.exists(file_path.value):
            with open(file_path.value, "r", encoding="utf-8") as file:
                lines = [line.rstrip("\n") for line in file if line.strip()]
            if 0 <= index < len(lines):
                del lines[index]
                with open(file_path.value, "w", encoding="utf-8") as file:
                    file.write("\n".join(lines))

    def load_openrouter_secret_key(self):
        try:
            # Attempt to load the secret key
            return self.read_file(RequiredString(OPENROUTER_SECRET_KEY_FILE))
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENROUTER_SECRET_KEY_FILE}'not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    def load_runpod_secret_key(self) -> RequiredString:
        try:
            # Attempt to load the secret key
            return self.read_file(RequiredString(RUNPOD_SECRET_KEY_FILE))
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{RUNPOD_SECRET_KEY_FILE}'not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def get_file_path_for_voice_line(
            character_name: RequiredString, voice_model: RequiredString
    ) -> (str, str):
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Generate a unique filename to prevent overwriting
        file_name = f"{timestamp}-{character_name}-{voice_model}.wav"

        # Note: the file name may have spaces. Because these files are supposed to be played by the client in a browser,
        # The spaces need to be replaced by %20.

        # Ensure the 'voice_lines' directory exists
        os.makedirs(VOICE_LINES_FOLDER_PATH, exist_ok=True)

        return os.path.join(VOICE_LINES_FOLDER_PATH, file_name)

    def load_openai_secret_key(self):
        try:
            # Attempt to load the secret key
            return self.read_file(RequiredString(OPENAI_SECRET_KEY_FILE))
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENAI_SECRET_KEY_FILE}' not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    def load_openai_project_key(self):
        try:
            # Attempt to load the secret key
            return self.read_file(RequiredString(OPENAI_PROJECT_KEY_FILE))
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENAI_PROJECT_KEY_FILE}' not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def get_temporary_folder_to_store_voice_parts(
            timestamp: RequiredString,
    ) -> RequiredString:
        temp_dir = os.path.join("temp_voice_lines", timestamp.value)
        os.makedirs(temp_dir, exist_ok=True)

        return RequiredString(temp_dir)

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

    def get_file_path_to_playthrough_folder(self, playthrough_name: RequiredString):
        if not isinstance(playthrough_name, RequiredString):
            playthrough_name = RequiredString(playthrough_name)

        return os.path.join(
            self.get_file_path_to_playthroughs_folder(), playthrough_name.value
        )

    def get_file_path_to_ongoing_dialogue(
            self, playthrough_name: RequiredString
    ) -> RequiredString:
        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthrough_folder(playthrough_name),
                ONGOING_DIALOGUE_FOLDER_NAME,
            )
        )

    def get_file_path_to_ongoing_dialogue_folder(
            self, playthrough_name: RequiredString
    ) -> RequiredString:
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        folder_path = self.get_file_path_to_ongoing_dialogue(playthrough_name)

        if not folder_path:
            os.makedirs(folder_path.value)

        return folder_path

    def get_file_path_to_interesting_situations(
        self, playthrough_name: RequiredString
    ) -> RequiredString:
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthrough_folder(playthrough_name),
                "interesting_situations.txt",
            )
        )

    def get_file_path_to_plot_twists(
            self, playthrough_name: RequiredString
    ) -> RequiredString:
        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthrough_folder(playthrough_name),
                "plot_twists.txt",
            )
        )

    def get_file_path_to_facts(
            self, playthrough_name: RequiredString
    ) -> RequiredString:
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthrough_folder(playthrough_name), "facts.txt"
            )
        )

    def get_file_path_to_interesting_dilemmas(
        self, playthrough_name: RequiredString
    ) -> RequiredString:
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthrough_folder(playthrough_name),
                "interesting_dilemmas.txt",
            )
        )

    def get_file_path_to_goals(
            self, playthrough_name: RequiredString
    ) -> RequiredString:
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthrough_folder(playthrough_name),
                "goals.txt",
            )
        )

    @staticmethod
    def get_file_path_to_empty_content_context_file() -> RequiredString:
        file_path = "errors"

        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        return RequiredString(os.path.join(file_path, "empty_content_context.txt"))

    def remove_ongoing_dialogue(self, playthrough_name: RequiredString):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        file_path = self.get_file_path_to_ongoing_dialogue(playthrough_name)

        if os.path.exists(file_path.value):
            os.remove(file_path.value)

    def get_file_path_to_playthrough_metadata(self, playthrough_name: RequiredString):
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            PLAYTHROUGH_METADATA_FILE,
        )

    def get_file_path_to_adventure(self, playthrough_name: RequiredString):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            "adventure.txt",
        )

    def get_file_path_to_plot_blueprints(
            self, playthrough_name: RequiredString
    ) -> RequiredString:
        if not isinstance(playthrough_name, RequiredString):
            raise TypeError(
                f"Expected playthrough_name to be PlaythroughName, but it was {type(playthrough_name)}."
            )

        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthrough_folder(playthrough_name),
                "plot_blueprints.txt",
            )
        )

    def get_file_path_to_map(self, playthrough_name: RequiredString) -> RequiredString:
        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthrough_folder(playthrough_name), MAP_FILE
            )
        )

    def get_file_path_to_characters(
            self, playthrough_name: RequiredString
    ) -> RequiredString:
        if not isinstance(playthrough_name, RequiredString):
            playthrough_name = RequiredString(playthrough_name)

        return RequiredString(
            os.path.join(
                self.get_file_path_to_playthroughs_folder(),
                playthrough_name.value,
                CHARACTERS_FOLDER_NAME,
            )
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
            playthrough_name: RequiredString, character_identifier: RequiredString
    ):
        return f"playthroughs/{playthrough_name}/{IMAGES_FOLDER_NAME}/{character_identifier}.png"

    def get_file_path_to_characters_file(self, playthrough_name: RequiredString):
        # Build the path to the characters folder
        characters_folder = self.get_file_path_to_characters(playthrough_name)
        os.makedirs(characters_folder.value, exist_ok=True)

        # Build the path to the characters.json file
        return os.path.join(characters_folder.value, CHARACTERS_FILE)

    def get_file_path_to_character_folder(
            self,
            playthrough_name: RequiredString,
            character_identifier: RequiredString,
            character_name: RequiredString,
    ):
        folder_name = f"{character_name} - {character_identifier}"
        file_path = os.path.join(
            self.get_file_path_to_characters(playthrough_name).value, folder_name
        )

        # Create the folder if it doesn't exist
        os.makedirs(file_path, exist_ok=True)

        return file_path

    def get_file_path_to_character_dialogues(
            self,
            playthrough_name: RequiredString,
            character_identifier: RequiredString,
            character_name: RequiredString,
    ):
        # Define the path
        folder_path = self.get_file_path_to_character_folder(
            playthrough_name, character_identifier, character_name
        )

        # Define the path to the "dialogues.txt" file
        return os.path.join(folder_path, DIALOGUES_FILE)

    def get_file_path_to_character_memories(
            self,
            playthrough_name: RequiredString,
            character_identifier: RequiredString,
            character_name: RequiredString,
    ):
        # Define the path to the "memories.txt" file
        return os.path.join(
            self.get_file_path_to_character_folder(
                playthrough_name, character_identifier, character_name
            ),
            MEMORIES_FILE,
        )

    def get_logging_config_file(self) -> dict:
        return self.load_existing_or_new_json_file(RequiredString(LOGGING_CONFIG_FILE))

    def create_playthrough_folder(self, playthrough_name: RequiredString) -> None:
        """
        Create a folder for the new playthrough.
        """
        path = self.get_file_path_to_playthrough_folder(playthrough_name)
        os.makedirs(path, exist_ok=False)
