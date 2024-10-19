from typing import Optional

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.dialogues.participants import Participants


class ParticipantsManager:
    def __init__(
        self,
        playthrough_name: str,
        character_manager: Optional[CharactersManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_manager = character_manager or CharactersManager(
            self._playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def initialize_participants(self) -> Participants:
        participants = Participants()

        player_id = self._playthrough_manager.get_player_identifier()

        player = Character(self._playthrough_name, player_id)

        participants.add_participant(
            player.identifier,
            player.get_attribute("name"),
            player.get_attribute("description"),
            player.get_attribute("personality"),
            player.get_attribute("equipment"),
            player.get_attribute("voice_model"),
        )

        followers = self._character_manager.get_followers()
        for follower in followers:
            participants.add_participant(
                follower.identifier,
                follower.get_attribute("name"),
                follower.get_attribute("description"),
                follower.get_attribute("personality"),
                follower.get_attribute("equipment"),
                follower.get_attribute("voice_model"),
            )

        return participants
