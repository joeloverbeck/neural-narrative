import os

from flask import url_for

from src.filesystem.filesystem_manager import FilesystemManager
from src.identifiers_manager import IdentifiersManager
from src.playthrough_manager import PlaythroughManager


class CharactersManager:

    def __init__(self, playthrough_name: str, filesystem_manager: FilesystemManager = None,
                 identifiers_manager: IdentifiersManager = None, playthrough_manager: PlaythroughManager = None):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(self._playthrough_name)

    def get_latest_character_identifier(self) -> str:
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(self._playthrough_name))

        return self._identifiers_manager.get_highest_identifier(characters_file)

    def get_character_data(self, character_identifier: str) -> dict:
        """
                Returns a dictionary with the 'name,' 'description,' 'personality,' and 'equipment'
                of the character corresponding to the given identifier.

                :param character_identifier: The identifier of the character as a string.
                :return: A dictionary containing the specified fields of the character.
                :raises ValueError: If the character identifier does not exist.
                """
        # Load the characters JSON file
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(self._playthrough_name))

        # Retrieve the character data for the given identifier
        character_data = characters_file.get(character_identifier)

        if not character_data:
            raise ValueError(f"Character with identifier '{character_identifier}' not found.")

        # Extract the required fields
        required_fields = ["name", "description", "personality", "equipment"]
        character_data = {field: character_data[field] for field in required_fields if field in character_data}

        character_data['image_url'] = url_for('static',
                                              filename=f'playthroughs/{self._playthrough_name}/images/{character_identifier}.png')

        return character_data

    def get_characters_at_current_place(self):
        # Get the current place identifier
        current_place = self._playthrough_manager.get_current_place()

        # Load the map file
        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name))

        # Get the current place data
        current_place_data = map_file.get(current_place, {})
        character_identifiers = current_place_data.get('characters', [])

        # Retrieve data for each character
        characters = []
        for character_id in character_identifiers:
            character_data = self.get_character_data(character_id)
            character_data['id'] = character_id  # Include the identifier
            # Assume images are stored in 'static/images/characters/<character_id>.png'
            character_data['image_url'] = url_for('static',
                                                  filename=f'playthroughs/{self._playthrough_name}/images/{character_id}.png')
            characters.append(character_data)

        return characters

    def load_character_data(self, playthrough_name: str, character_identifier: str):
        # Define the path
        file_path = self._filesystem_manager.get_file_path_to_characters_file(playthrough_name)

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at path {file_path} does not exist.")

        # Load the JSON data from the file
        characters_data = self._filesystem_manager.read_json_file(file_path)

        # Return the character data for the given identifier
        if str(character_identifier) not in characters_data:
            raise KeyError(f"Character with identifier '{character_identifier}' not found.")

        return characters_data[str(character_identifier)]

    def load_character_memories(self, playthrough_name: str, character_identifier: str):
        character_data = self.load_character_data(playthrough_name, character_identifier)

        file_path = self._filesystem_manager.get_file_path_to_character_memories(playthrough_name, character_identifier,
                                                                                 character_data)

        # Check if the file exists, and if not, create an empty file
        self._filesystem_manager.create_empty_file_if_not_exists(file_path)

        return self._filesystem_manager.read_file(file_path)
