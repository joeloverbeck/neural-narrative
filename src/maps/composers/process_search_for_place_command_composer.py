from src.base.validators import validate_non_empty_string
from src.maps.commands.process_search_for_place_command import (
    ProcessSearchForPlaceCommand,
)
from src.maps.commands.search_for_place_command import SearchForPlaceCommand
from src.maps.composers.random_template_type_map_entry_provider_factory_composer import (
    RandomTemplateTypeMapEntryProviderFactoryComposer,
)
from src.maps.factories.attach_place_command_factory import AttachPlaceCommandFactory
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class ProcessSearchForPlaceCommandComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_command(self) -> ProcessSearchForPlaceCommand:
        random_template_type_map_entry_provider_factory = (
            RandomTemplateTypeMapEntryProviderFactoryComposer(
                self._playthrough_name
            ).compose_factory()
        )

        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        map_manager_factory = MapManagerFactory(self._playthrough_name)

        search_for_place_command = SearchForPlaceCommand(
            self._playthrough_name,
            random_template_type_map_entry_provider_factory,
            place_manager_factory,
            map_manager_factory,
        )

        attach_place_command_factory = AttachPlaceCommandFactory(
            self._playthrough_name, place_manager_factory
        )

        return ProcessSearchForPlaceCommand(
            search_for_place_command, attach_place_command_factory, map_manager_factory
        )
