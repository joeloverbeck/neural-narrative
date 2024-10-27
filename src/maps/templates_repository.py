from typing import Dict, Optional

from src.base.enums import TemplateType
from src.filesystem.file_operations import (
    read_json_file,
    write_json_file,
    create_directories,
    create_empty_json_file_if_not_exists,
)
from src.filesystem.path_manager import PathManager


class TemplatesRepository:
    def __init__(self, path_manager: Optional[PathManager] = None):
        self._path_manager = path_manager or PathManager()

    def load_templates(self, place_type: TemplateType) -> Dict:
        # Ensure templates dir exists.
        create_directories(self._path_manager.TEMPLATES_DIR)

        file_path = self._path_manager.get_templates_paths(place_type)

        # Ensure the file exists.
        create_empty_json_file_if_not_exists(file_path)

        templates = read_json_file(file_path)

        return templates

    def save_templates(self, place_type: TemplateType, templates: Dict) -> None:
        # Save regular templates
        file_path = self._path_manager.get_templates_paths(place_type)
        write_json_file(file_path, templates)
