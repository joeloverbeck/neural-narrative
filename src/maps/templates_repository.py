import os.path
from typing import Dict, Optional

from src.base.enums import TemplateType
from src.filesystem.file_operations import read_json_file, write_json_file
from src.filesystem.path_manager import PathManager


class TemplatesRepository:
    def __init__(self, path_manager: Optional[PathManager] = None):
        self._path_manager = path_manager or PathManager()

    def load_templates(self, place_type: TemplateType) -> Dict:
        file_path = self._path_manager.get_templates_paths(place_type)

        templates = read_json_file(file_path)

        # Must load the secret templates as well.
        secret_templates_file_path = self._path_manager.get_templates_paths(
            place_type, secret=True
        )

        if os.path.exists(secret_templates_file_path):
            templates.update(read_json_file(secret_templates_file_path))

        return templates

    def save_templates(self, place_type: TemplateType, templates: Dict) -> None:
        secret_templates = {}

        for key in templates.keys():
            if "secret" in templates[key]:
                secret_templates.update(templates.pop(key))

        # Save regular templates
        file_path = self._path_manager.get_templates_paths(place_type)
        write_json_file(file_path, templates)

        # Save secret templates
        file_path = self._path_manager.get_templates_paths(place_type, secret=True)
        write_json_file(file_path, secret_templates)
