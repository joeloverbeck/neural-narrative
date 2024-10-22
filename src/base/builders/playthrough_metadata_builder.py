from typing import Optional, List


class PlaythroughMetadataBuilder:

    def __init__(self):
        self._metadata = {'story_universe_template': Optional[str],
                          'player_identifier': Optional[str], 'current_place': Optional[
                str], 'time': {}, 'last_identifiers': {}, 'followers': []}

    def set_story_universe_template(self, template: str):
        self._metadata['story_universe_template'] = template
        return self

    def set_player_identifier(self, character_identifier: str):
        self._metadata['player_identifier'] = character_identifier
        return self

    def set_followers(self, followers: Optional[List[str]] = None):
        self._metadata['followers'] = followers or []
        return self

    def set_current_place(self, place_identifier: str):
        self._metadata['current_place'] = place_identifier
        return self

    def set_time_hour(self, hour: int):
        self._metadata['time']['hour'] = hour
        return self

    def set_last_identifiers(self, places: str, characters: str):
        self._metadata['last_identifiers']['places'] = places
        self._metadata['last_identifiers']['characters'] = characters
        return self

    def build(self):
        return self._metadata
