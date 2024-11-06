from typing import List, Dict, Optional

from src.base.identifiers_manager import IdentifiersManager
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.characters.character import Character
from src.filesystem.file_operations import (
    read_json_file,
    create_directories,
    create_empty_json_file_if_not_exists,
)
from src.filesystem.path_manager import PathManager
from src.maps.map_repository import MapRepository


class CharactersManager:

    def __init__(
        self,
        playthrough_name: str,
        identifiers_manager: Optional[IdentifiersManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        map_repository: Optional[MapRepository] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_manager")

        self._playthrough_name = playthrough_name

        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._map_repository = map_repository or MapRepository(self._playthrough_name)
        self._path_manager = path_manager or PathManager()

    def _load_characters_file(self) -> Dict[str, Dict]:
        # It could be that the characters directory doesn't yet exist.
        characters_path = self._path_manager.get_characters_path(self._playthrough_name)
        create_directories(characters_path)

        # It could be that the characters file doesn't yet exist.
        characters_file_path = self._path_manager.get_characters_file_path(
            self._playthrough_name
        )

        create_empty_json_file_if_not_exists(characters_file_path)

        return read_json_file(characters_file_path)

    def get_latest_character_identifier(self) -> str:
        characters_file = self._load_characters_file()

        return self._identifiers_manager.get_highest_identifier(characters_file)

    def get_characters(self, character_identifiers: List[str]) -> List[Character]:
        return [
            Character(self._playthrough_name, identifier)
            for identifier in character_identifiers
        ]

    def get_followers(self) -> List[Character]:
        return self.get_characters(self._playthrough_manager.get_followers())

    def get_characters_at_current_place(self) -> List[Character]:
        current_place = self._playthrough_manager.get_current_place_identifier()
        map_file = self._map_repository.load_map_data()

        current_place_data = map_file.get(current_place, {})
        character_ids = current_place_data.get("characters", [])

        return self.get_characters(character_ids)

    def get_characters_at_current_place_plus_followers(self) -> List[Character]:
        characters = self.get_characters_at_current_place()
        characters.extend(self.get_followers())
        return characters

    def get_all_characters(self) -> List[dict]:
        characters_file = self._load_characters_file()
        return [
            {"identifier": identifier, "name": data.get("name", "Unknown")}
            for identifier, data in characters_file.items()
        ]

    def get_all_character_names(self) -> List[str]:
        characters_file = self._load_characters_file()
        return [data.get("name", "") for data in characters_file.values()]

    @staticmethod
    def get_characters_info(characters: List[Character], role: str) -> Optional[str]:
        followers_info = ""
        for follower in characters:
            followers_info += follower.get_info_for_prompt(role)
        if not followers_info:
            return None
        return followers_info
