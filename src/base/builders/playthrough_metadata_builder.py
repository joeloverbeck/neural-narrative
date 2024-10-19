class PlaythroughMetadataBuilder:
    def __init__(self):
        self._metadata = {
            "world_template": None,
            "player_identifier": None,
            "current_place": None,
            "time": {},
            "last_identifiers": {},
        }

    def set_world_template(self, template):
        self._metadata["world_template"] = template
        return self

    def set_player_identifier(self, character_identifier):
        self._metadata["player_identifier"] = character_identifier
        return self

    def set_followers(self):
        self._metadata["followers"] = []
        return self

    def set_current_place(self, place_identifier):
        self._metadata["current_place"] = place_identifier
        return self

    def set_time_hour(self, hour):
        self._metadata["time"]["hour"] = hour
        return self

    def set_last_identifiers(self, places, characters):
        self._metadata["last_identifiers"]["places"] = places
        self._metadata["last_identifiers"]["characters"] = characters
        return self

    def build(self):
        return self._metadata
