import logging.config
from typing import Optional, Dict, Any
from src.base.abstracts.command import Command
from src.base.constants import PARENT_KEYS
from src.base.enums import IdentifierType, TemplateType
from src.base.identifiers_manager import IdentifiersManager
from src.filesystem.filesystem_manager import FilesystemManager
logger = logging.getLogger(__name__)


class CreateMapEntryForPlaythroughCommand(Command):

    def __init__(self, playthrough_name: str, father_identifier: Optional[
        str], place_type: TemplateType, place_template: str,
                 filesystem_manager: Optional[FilesystemManager] = None,
                 identifiers_manager: Optional[IdentifiersManager] = None):
        self._playthrough_name = playthrough_name
        self._father_identifier = father_identifier
        self._place_type = place_type
        self._place_template = place_template
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            self._playthrough_name)

    def _get_parent_key(self) -> Optional[str]:
        """Get the parent key based on the place type."""
        return PARENT_KEYS.get(self._place_type)

    def _get_additional_fields(self) -> Dict[str, Any]:
        """Get additional fields required based on the place type."""
        additional_fields: Dict[str, Any] = {}
        if self._place_type == TemplateType.AREA:
            additional_fields.update({'weather_identifier': 'sunny',
                                      'locations': [], 'characters': [], 'visited': False})
        elif self._place_type == TemplateType.LOCATION:
            additional_fields.update({'characters': [], 'visited': False})
        return additional_fields

    def execute(self) -> None:
        """Create a map entry for the playthrough using the selected place."""
        map_file = self._filesystem_manager.load_existing_or_new_json_file(self
                                                                           ._filesystem_manager.get_file_path_to_map(
            self._playthrough_name))
        new_id = self._identifiers_manager.produce_and_update_next_identifier(
            IdentifierType.PLACES)
        map_entry = {'type': self._place_type, 'place_template': self.
        _place_template}
        parent_key = self._get_parent_key()
        if parent_key:
            if not self._father_identifier:
                raise ValueError(
                    f"When creating a map entry for '{self._place_type}', the father's identifier is required but was not provided."
                )
            map_entry[parent_key] = self._father_identifier
        additional_fields = self._get_additional_fields()
        map_entry.update(additional_fields)
        map_file[str(new_id)] = map_entry
        self._filesystem_manager.save_json_file(map_file, self.
                                                _filesystem_manager.get_file_path_to_map(self._playthrough_name))
        logger.info(
            f"Map entry created for playthrough '{self._playthrough_name}' with {self._place_type} '{self._place_template}'."
        )
