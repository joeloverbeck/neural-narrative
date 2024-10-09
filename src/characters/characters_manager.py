from typing import List

from src.constants import CHARACTER_GENERATION_GUIDELINES_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.identifiers_manager import IdentifiersManager
from src.playthrough_manager import PlaythroughManager


class CharactersManager:

    def __init__(
        self,
        playthrough_name: str,
        filesystem_manager: FilesystemManager = None,
        identifiers_manager: IdentifiersManager = None,
        playthrough_manager: PlaythroughManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def get_latest_character_identifier(self) -> str:
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(
                self._playthrough_name
            )
        )

        return self._identifiers_manager.get_highest_identifier(characters_file)

    def load_character_data(self, character_identifier: str) -> dict:
        if not isinstance(character_identifier, str):
            raise TypeError(
                f"Attempted to load the character data with a non-string identifier. Identifier type: {type(character_identifier)}"
            )

        # Load the characters JSON file
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(
                self._playthrough_name
            )
        )

        # Return the character data for the given identifier
        if character_identifier not in characters_file:
            raise KeyError(
                f"Character with identifier '{character_identifier}' not found."
            )

        character_data = characters_file[character_identifier]

        character_data["identifier"] = character_identifier
        character_data["image_url"] = (
            self._filesystem_manager.get_file_path_to_character_image_for_web(
                self._playthrough_name, character_identifier
            )
        )

        return character_data

    def get_full_data_of_characters(
        self, character_identifiers: List[str]
    ) -> List[dict]:
        # Retrieve data for each character
        characters = []

        for character_identifier in character_identifiers:
            character_data = self.load_character_data(character_identifier)
            characters.append(character_data)

        return characters

    def get_followers(self) -> List[dict]:
        return self.get_full_data_of_characters(
            self._playthrough_manager.get_followers()
        )

    def get_characters_at_current_place(self):
        # Get the current place identifier
        current_place = self._playthrough_manager.get_current_place_identifier()

        # Load the map file
        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name)
        )

        # Get the current place data
        current_place_data = map_file.get(current_place, {})

        characters = self.get_full_data_of_characters(
            current_place_data.get("characters", [])
        )

        return characters

    def get_characters_at_current_place_plus_followers(self):
        characters = self.get_characters_at_current_place()

        # Add to that the player's followers.
        followers = self.get_full_data_of_characters(
            PlaythroughManager(self._playthrough_name).get_followers()
        )

        characters.extend(followers)

        return characters

    def load_character_memories(self, character_identifier: str) -> str:
        character_data = self.load_character_data(character_identifier)

        file_path = self._filesystem_manager.get_file_path_to_character_memories(
            self._playthrough_name, character_identifier, character_data["name"]
        )

        # Check if the file exists, and if not, create an empty file
        self._filesystem_manager.create_empty_file_if_not_exists(file_path)

        return self._filesystem_manager.read_file(file_path)

    def get_voice_model(self, character_identifier: str) -> str:
        character_data = self.load_character_data(character_identifier)

        if "voice_model" not in character_data:
            raise ValueError(
                f"Found a character without 'voice_model':\n{character_data}"
            )

        return character_data["voice_model"]

    def get_all_characters(self) -> List[dict]:
        """Returns a list of all characters with their identifiers and names."""
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(
                self._playthrough_name
            )
        )

        all_characters = []
        for identifier, data in characters_file.items():
            character = {
                "identifier": identifier,
                "name": data.get("name", "Unknown"),
            }
            all_characters.append(character)
        return all_characters

    def save_character_memories(self, character_identifier: str, memories: str):
        """Saves the given memories to the character's memories file."""
        character_data = self.load_character_data(character_identifier)
        character_name = character_data["name"]

        file_path = self._filesystem_manager.get_file_path_to_character_memories(
            self._playthrough_name, character_identifier, character_name
        )
        self._filesystem_manager.write_file(file_path, memories)

    def get_all_character_names(self) -> List[str]:
        """
        Returns a list of all character names in the characters.json file.
        """
        # Load the characters JSON file
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(
                self._playthrough_name
            )
        )

        # Extract and return the names
        return [char_data.get("name", "") for char_data in characters_file.values()]

    @staticmethod
    def create_key_for_character_generation_guidelines(
        world: str, region: str, area: str, location: str = None
    ) -> str:
        if not world:
            raise ValueError("world can't be empty.")
        if not region:
            raise ValueError("region can't be empty.")
        if not area:
            raise ValueError("area can't be empty.")

        return (
            f"{world}:{region}:{area}:{location}"
            if location
            else f"{world}:{region}:{area}"
        )

    def load_character_generation_guidelines(
        self, world: str, region: str, area: str, location: str = None
    ) -> List[str]:
        if not world:
            raise ValueError("world can't be empty.")
        if not region:
            raise ValueError("region can't be empty.")
        if not area:
            raise ValueError("area can't be empty.")

        guidelines_file = self._filesystem_manager.load_existing_or_new_json_file(
            CHARACTER_GENERATION_GUIDELINES_FILE
        )

        key = self.create_key_for_character_generation_guidelines(
            world, region, area, location
        )

        if not key in guidelines_file:
            raise ValueError(
                f"The key {key} wasn't present in the file of character generation guidelines. You should ask first if there's a matching entry."
            )

        return guidelines_file[key]

    def save_character_generation_guidelines(
        self,
        world: str,
        region: str,
        area: str,
        guidelines: List[str],
        location: str = None,
    ):
        if not world:
            raise ValueError("world can't be empty.")
        if not region:
            raise ValueError("region can't be empty.")
        if not area:
            raise ValueError("area can't be empty.")

        guidelines_file = self._filesystem_manager.load_existing_or_new_json_file(
            CHARACTER_GENERATION_GUIDELINES_FILE
        )

        guidelines_file[
            self.create_key_for_character_generation_guidelines(
                world, region, area, location
            )
        ] = guidelines

        self._filesystem_manager.save_json_file(
            guidelines_file,
            CHARACTER_GENERATION_GUIDELINES_FILE,
        )

    def are_there_character_generation_guidelines_for_place(
        self, world: str, region: str, area: str, location: str = None
    ) -> bool:
        if not world:
            raise ValueError("world can't be empty.")
        if not region:
            raise ValueError("region can't be empty.")
        if not area:
            raise ValueError("area can't be empty.")

        guidelines_file = self._filesystem_manager.load_existing_or_new_json_file(
            CHARACTER_GENERATION_GUIDELINES_FILE
        )

        return (
            self.create_key_for_character_generation_guidelines(
                world, region, area, location
            )
            in guidelines_file
        )
