from typing import Optional, Dict

from src.base.constants import (
    TEMPLATE_FILES,
)
from src.base.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager


class TemplatesRepository:
    def __init__(self, filesystem_manager: Optional[FilesystemManager] = None):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def load_template(self, place_type: TemplateType) -> Dict:
        file_path = TEMPLATE_FILES.get(place_type)

        if not file_path:
            raise ValueError(
                f"Template file for place type '{place_type.value}' not found."
            )

        return self._filesystem_manager.load_existing_or_new_json_file(file_path)
