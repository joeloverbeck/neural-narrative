import logging

from src.base.playthrough_manager import PlaythroughManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_manager_factory import PlaceManagerFactory

logger = logging.getLogger(__name__)


class MovementManager:

    def __init__(
        self,
        playthrough_name: str,
        place_manager_factory: PlaceManagerFactory,
        playthrough_manager: PlaythroughManager = None,
        filesystem_manager: FilesystemManager = None,
    ):
        self._playthrough_name = playthrough_name
        self._place_manager_factory = place_manager_factory
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def add_follower(
        self, character_identifier: str, current_place_identifier: str
    ) -> None:
        self._playthrough_manager.add_follower(character_identifier)
        self._place_manager_factory.create_place_manager().remove_character_from_place(
            character_identifier, current_place_identifier
        )
