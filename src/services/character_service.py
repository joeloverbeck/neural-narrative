from src.movements.movement_manager import MovementManager
from src.playthrough_manager import PlaythroughManager


class CharacterService:
    @staticmethod
    def add_followers(playthrough_name, character_ids):
        movement_manager = MovementManager(playthrough_name)
        playthrough_manager = PlaythroughManager(playthrough_name)
        for character_id in character_ids:
            movement_manager.add_follower(
                character_id, playthrough_manager.get_current_place_identifier()
            )

    @staticmethod
    def remove_followers(playthrough_name, follower_ids):
        movement_manager = MovementManager(playthrough_name)
        playthrough_manager = PlaythroughManager(playthrough_name)
        for follower_id in follower_ids:
            movement_manager.remove_follower(
                follower_id, playthrough_manager.get_current_place_identifier()
            )
