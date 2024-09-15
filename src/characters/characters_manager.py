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

    def load_character_data(self, character_identifier: str):
        if not isinstance(character_identifier, str):
            raise TypeError(
                f"Attempted to load the character data with a non-string identifier. Identifier type: {type(character_identifier)}")

        # Load the characters JSON file
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(self._playthrough_name))

        # Return the character data for the given identifier
        if character_identifier not in characters_file:
            raise KeyError(f"Character with identifier '{character_identifier}' not found.")

        character_data = characters_file[character_identifier]

        character_data['identifier'] = character_identifier
        character_data['image_url'] = self._filesystem_manager.get_file_path_to_character_image_for_web(
            self._playthrough_name, character_identifier)

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

        for character_identifier in character_identifiers:
            character_data = self.load_character_data(character_identifier)
            characters.append(character_data)

        return characters

    def load_character_memories(self, playthrough_name: str, character_identifier: str):
        character_data = self.load_character_data(character_identifier)

        file_path = self._filesystem_manager.get_file_path_to_character_memories(playthrough_name, character_identifier,
                                                                                 character_data)

        # Check if the file exists, and if not, create an empty file
        self._filesystem_manager.create_empty_file_if_not_exists(file_path)

        return self._filesystem_manager.read_file(file_path)
