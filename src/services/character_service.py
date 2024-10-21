from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString
from src.characters.factories.generate_character_command_factory_composer import (
    GenerateCharacterCommandFactoryComposer,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.movement_manager import MovementManager


class CharacterService:
    @staticmethod
    def add_followers(playthrough_name, character_ids):
        place_manager_factory = PlaceManagerFactory(RequiredString(playthrough_name))
        movement_manager = MovementManager(playthrough_name, place_manager_factory)
        playthrough_manager = PlaythroughManager(playthrough_name)
        for character_id in character_ids:
            movement_manager.add_follower(
                character_id, playthrough_manager.get_current_place_identifier()
            )

    @staticmethod
    def remove_followers(playthrough_name, follower_ids):
        place_manager_factory = PlaceManagerFactory(RequiredString(playthrough_name))
        movement_manager = MovementManager(playthrough_name, place_manager_factory)
        playthrough_manager = PlaythroughManager(playthrough_name)
        for follower_id in follower_ids:
            movement_manager.remove_follower(
                follower_id, playthrough_manager.get_current_place_identifier()
            )

    @staticmethod
    def generate_character(playthrough_name: RequiredString, guideline: RequiredString):
        playthrough_manager = PlaythroughManager(playthrough_name)
        places_templates_parameter = (
            HierarchyManagerFactory(playthrough_name)
            .create_hierarchy_manager()
            .fill_places_templates_parameter(
                RequiredString(playthrough_manager.get_current_place_identifier())
            )
        )

        # Generate the character
        GenerateCharacterCommandFactoryComposer(
            playthrough_name
        ).compose_factory().create_generate_character_command(
            places_templates_parameter,
            place_character_at_current_place=True,
            user_content=guideline.value,
        ).execute()
