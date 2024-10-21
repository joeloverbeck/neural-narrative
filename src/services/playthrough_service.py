from src.base.commands.create_playthrough_command import CreatePlaythroughCommand
from src.base.commands.create_playthrough_metadata_command import (
    CreatePlaythroughMetadataCommand,
)
from src.base.required_string import RequiredString
from src.characters.commands.generate_player_character_command import (
    GeneratePlayerCharacterCommand,
)
from src.characters.factories.generate_character_command_factory_composer import (
    GenerateCharacterCommandFactoryComposer,
)
from src.maps.commands.create_initial_map_command import CreateInitialMapCommand
from src.maps.composers.random_template_type_map_entry_provider_factory_composer import (
    RandomTemplateTypeMapEntryProviderFactoryComposer,
)
from src.maps.composers.visit_place_command_factory_composer import (
    VisitPlaceCommandFactoryComposer,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.map_manager_factory import MapManagerFactory


class PlaythroughService:

    @staticmethod
    def create_playthrough(
        playthrough_name: RequiredString,
        story_universe_template: RequiredString,
        player_notion: RequiredString,
    ):
        # Instantiate necessary commands and factories
        create_playthrough_metadata_command = CreatePlaythroughMetadataCommand(
            playthrough_name, story_universe_template
        )

        map_manager_factory = MapManagerFactory(playthrough_name)

        random_template_type_map_entry_provider_factory = (
            RandomTemplateTypeMapEntryProviderFactoryComposer(
                playthrough_name
            ).compose_factory()
        )

        create_initial_map_command = CreateInitialMapCommand(
            story_universe_template,
            random_template_type_map_entry_provider_factory,
            map_manager_factory,
        )

        generate_character_command_factory = GenerateCharacterCommandFactoryComposer(
            playthrough_name
        ).compose_factory()

        hierarchy_manager_factory = HierarchyManagerFactory(playthrough_name)

        generate_player_character_command = GeneratePlayerCharacterCommand(
            playthrough_name,
            player_notion,
            generate_character_command_factory,
            hierarchy_manager_factory,
        )

        visit_place_command_factory = VisitPlaceCommandFactoryComposer(
            playthrough_name
        ).compose_factory()

        CreatePlaythroughCommand(
            create_playthrough_metadata_command,
            create_initial_map_command,
            generate_player_character_command,
            visit_place_command_factory,
            map_manager_factory,
        ).execute()
