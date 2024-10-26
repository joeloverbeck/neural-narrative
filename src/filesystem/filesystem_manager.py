import json
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict

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
    ONGOING_DIALOGUE_FILE,
    RUNPOD_SECRET_KEY_FILE,
    VOICE_LINES_FOLDER_PATH,
)
from src.filesystem.file_operations import read_file, read_json_file

logger = logging.getLogger(__name__)


class FilesystemManager:

    @staticmethod
    def create_empty_file_if_not_exists(file_path: str) -> None:
        """Create an empty file if it does not exist."""
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8"):
                pass

    @staticmethod
    def write_binary_file(file_path: str, contents: bytes) -> None:
        """Write binary contents to a file."""
        with open(file_path, "wb") as f:
            f.write(contents)

    @staticmethod
    def save_json_file(json_data: Dict | List[Dict], file_path: str) -> None:
        """Serialize json_data to a JSON-formatted file with proper encoding."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)  # noqa

    @staticmethod
    def remove_item_from_file(file_path: str, index: int):
        """Remove a line at a specific index from a file."""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                lines = [line.rstrip("\n") for line in file if line.strip()]
            if 0 <= index < len(lines):
                del lines[index]
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("\n".join(lines))

    @staticmethod
    def load_openrouter_secret_key():
        try:
            return read_file(Path(OPENROUTER_SECRET_KEY_FILE))
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENROUTER_SECRET_KEY_FILE}'not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def load_runpod_secret_key() -> str:
        try:
            return read_file(Path(RUNPOD_SECRET_KEY_FILE))
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{RUNPOD_SECRET_KEY_FILE}'not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def get_file_path_for_voice_line(character_name: str, voice_model: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{timestamp}-{character_name}-{voice_model}.wav"
        os.makedirs(VOICE_LINES_FOLDER_PATH, exist_ok=True)
        return os.path.join(VOICE_LINES_FOLDER_PATH, file_name)

    @staticmethod
    def load_openai_secret_key():
        try:
            return read_file(Path(OPENAI_SECRET_KEY_FILE))
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENAI_SECRET_KEY_FILE}' not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def load_openai_project_key():
        try:
            return read_file(Path(OPENAI_PROJECT_KEY_FILE))
        except FileNotFoundError:
            sys.exit(
                f"Error: File '{OPENAI_PROJECT_KEY_FILE}' not found. Please check the file path."
            )
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def get_temporary_folder_to_store_voice_parts(timestamp: str) -> str:
        temp_dir = os.path.join("temp_voice_lines", timestamp)
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    @staticmethod
    def get_file_path_to_playthroughs_folder():
        if not os.path.exists(PLAYTHROUGHS_FOLDER):
            os.makedirs(PLAYTHROUGHS_FOLDER)
        return PLAYTHROUGHS_FOLDER

    def get_playthrough_names(self) -> List[str]:
        playthroughs_folder = self.get_file_path_to_playthroughs_folder()
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

    def delete_playthrough_folder(self, playthrough_name: str) -> None:
        """
        Delete the playthrough folder for the given playthrough name.

        Args:
            playthrough_name (str): The name of the playthrough whose folder is to be deleted.
        """
        folder_path = self.get_file_path_to_playthrough_folder(playthrough_name)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                logger.info(f"Deleted playthrough folder at: {folder_path}")
            except Exception as e:
                logger.error(
                    f"Failed to delete playthrough folder at {folder_path}: {e}"
                )
                raise
        else:
            logger.warning(f"Playthrough folder does not exist at: {folder_path}")

    def get_file_path_to_ongoing_dialogue(self, playthrough_name: str) -> str:
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            ONGOING_DIALOGUE_FILE,
        )

    def get_file_path_to_interesting_situations(self, playthrough_name: str) -> str:
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            "scenarios.txt",
        )

    def get_file_path_to_plot_twists(self, playthrough_name: str) -> str:
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            "plot_twists.txt",
        )

    def get_file_path_to_facts(self, playthrough_name: str) -> str:
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name), "facts.txt"
        )

    def get_file_path_to_interesting_dilemmas(self, playthrough_name: str) -> str:
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            "dilemmas.txt",
        )

    def get_file_path_to_goals(self, playthrough_name: str) -> str:
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name), "goals.txt"
        )

    @staticmethod
    def get_file_path_to_empty_content_context_file() -> str:
        file_path = "errors"
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        return os.path.join(file_path, "empty_content_context.txt")

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
            self.get_file_path_to_playthrough_folder(playthrough_name), "adventure.txt"
        )

    def get_file_path_to_plot_blueprints(self, playthrough_name: str) -> str:
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name),
            "plot_blueprints.txt",
        )

    def get_file_path_to_map(self, playthrough_name: str) -> str:
        return os.path.join(
            self.get_file_path_to_playthrough_folder(playthrough_name), MAP_FILE
        )

    def get_file_path_to_characters(self, playthrough_name: str) -> str:
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
    ) -> str:
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
        characters_folder = self.get_file_path_to_characters(playthrough_name)
        os.makedirs(characters_folder, exist_ok=True)
        return os.path.join(characters_folder, CHARACTERS_FILE)

    def get_file_path_to_character_folder(
        self, playthrough_name: str, character_identifier: str, character_name: str
    ):
        folder_name = f"{character_name} - {character_identifier}"
        file_path = os.path.join(
            self.get_file_path_to_characters(playthrough_name), folder_name
        )
        os.makedirs(file_path, exist_ok=True)
        return file_path

    def get_file_path_to_character_dialogues(
        self, playthrough_name: str, character_identifier: str, character_name: str
    ):
        folder_path = self.get_file_path_to_character_folder(
            playthrough_name, character_identifier, character_name
        )
        return os.path.join(folder_path, DIALOGUES_FILE)

    def get_file_path_to_character_memories(
        self, playthrough_name: str, character_identifier: str, character_name: str
    ):
        return os.path.join(
            self.get_file_path_to_character_folder(
                playthrough_name, character_identifier, character_name
            ),
            MEMORIES_FILE,
        )

    @staticmethod
    def get_logging_config_file() -> dict:
        return read_json_file(Path(LOGGING_CONFIG_FILE))

    def create_playthrough_folder(self, playthrough_name: str) -> None:
        """
        Create a folder for the new playthrough.
        """
        path = self.get_file_path_to_playthrough_folder(playthrough_name)
        os.makedirs(path, exist_ok=False)

    @staticmethod
    def copy_file(origin_file_path: str, destination_file_path: str):
        shutil.copy(origin_file_path, destination_file_path)
