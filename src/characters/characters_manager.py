from typing import List, Dict, Optional
from src.base.identifiers_manager import IdentifiersManager
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.filesystem.filesystem_manager import FilesystemManager


class CharactersManager:

    def __init__(self, playthrough_name: str, filesystem_manager: Optional[
        FilesystemManager] = None, identifiers_manager: Optional[
        IdentifiersManager] = None, playthrough_manager: Optional[
        PlaythroughManager] = None):
        if not playthrough_name:
            raise ValueError('playthrough_name should not be empty.')
        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name)

    def _load_characters_file(self) -> Dict[str, Dict]:
        return self._filesystem_manager.load_existing_or_new_json_file(self
                                                                       ._filesystem_manager.get_file_path_to_characters_file(
            self.
            _playthrough_name))

    def _load_map_file(self) -> Dict[str, Dict]:
        return self._filesystem_manager.load_existing_or_new_json_file(self
                                                                       ._filesystem_manager.get_file_path_to_map(
            self._playthrough_name))

    def get_latest_character_identifier(self) -> str:
        characters_file = self._load_characters_file()
        return self._identifiers_manager.get_highest_identifier(characters_file
                                                                )

    def get_characters(self, character_identifiers: List[str]) -> List[Character
    ]:
        return [Character(self._playthrough_name, identifier) for
                identifier in character_identifiers]

    def get_followers(self) -> List[Character]:
        return self.get_characters(self._playthrough_manager.get_followers())

    def get_characters_at_current_place(self) -> List[Character]:
        current_place = self._playthrough_manager.get_current_place_identifier(
        )
        map_file = self._load_map_file()
        current_place_data = map_file.get(current_place, {})
        character_ids = current_place_data.get('characters', [])
        return self.get_characters(character_ids)

    def get_characters_at_current_place_plus_followers(self) -> List[Character]:
        characters = self.get_characters_at_current_place()
        characters.extend(self.get_followers())
        return characters

    def get_all_characters(self) -> List[dict]:
        characters_file = self._load_characters_file()
        return [{'identifier': identifier, 'name': data.get('name',
                                                            'Unknown')} for identifier, data in characters_file.items()]

    def get_all_character_names(self) -> List[str]:
        characters_file = self._load_characters_file()
        return [data.get('name', '') for data in characters_file.values()]
