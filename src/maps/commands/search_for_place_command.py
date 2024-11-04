from typing import Optional

from src.base.abstracts.command import Command
from src.base.constants import CHILD_TEMPLATE_TYPE
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType
from src.maps.exceptions import SearchForPlaceError
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.random_template_type_map_entry_provider_factory import (
    RandomTemplateTypeMapEntryProviderFactory,
)


class SearchForPlaceCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        random_template_type_map_entry_provider_factory: RandomTemplateTypeMapEntryProviderFactory,
        place_manager_factory: PlaceManagerFactory,
        map_manager_factory: MapManagerFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._random_template_type_map_entry_provider_factory = (
            random_template_type_map_entry_provider_factory
        )
        self._place_manager_factory = place_manager_factory
        self._map_manager_factory = map_manager_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        father_template = (
            self._map_manager_factory.create_map_manager().get_current_place_template()
        )

        father_identifier = self._playthrough_manager.get_current_place_identifier()

        current_place_type = (
            self._place_manager_factory.create_place_manager().get_current_place_type()
        )

        child_place_type = CHILD_TEMPLATE_TYPE.get(current_place_type)

        random_template_type_map_entry_provider = (
            self._random_template_type_map_entry_provider_factory.create_provider(
                father_identifier, father_template, current_place_type, child_place_type
            )
        )

        result = random_template_type_map_entry_provider.create_map_entry()

        if (
            result.get_result_type()
            == RandomTemplateTypeMapEntryCreationResultType.FAILURE
        ):
            raise SearchForPlaceError(
                f"The search for a place failed for an unknown reason."
            )

        if (
            result.get_result_type()
            == RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
        ):
            raise SearchForPlaceError(
                f"The search for a place failed because there were no available templates."
            )
