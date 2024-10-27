from src.base.playthrough_manager import PlaythroughManager
from src.characters.factories.generate_character_command_factory_composer import (
    GenerateCharacterCommandFactoryComposer,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)
from src.movements.movement_manager import MovementManager


class CharacterService:

    @staticmethod
    def add_followers(playthrough_name, character_ids):
        place_manager_factory = PlaceManagerFactory(playthrough_name)
        movement_manager = MovementManager(playthrough_name, place_manager_factory)
        playthrough_manager = PlaythroughManager(playthrough_name)
        for character_id in character_ids:
            movement_manager.add_follower(
                character_id, playthrough_manager.get_current_place_identifier()
            )

    @staticmethod
    def remove_followers(playthrough_name, follower_ids):
        playthrough_manager = PlaythroughManager(playthrough_name)

        for follower_id in follower_ids:
            playthrough_manager.remove_follower(follower_id)
            PlaceCharacterAtPlaceCommandFactory(playthrough_name).create_command(
                follower_id, playthrough_manager.get_current_place_identifier()
            ).execute()

    @staticmethod
    def generate_character(playthrough_name: str, guideline: str):
        GenerateCharacterCommandFactoryComposer(
            playthrough_name
        ).compose_factory().create_generate_character_command(
            place_character_at_current_place=True,
            user_content=guideline,
        ).execute()
