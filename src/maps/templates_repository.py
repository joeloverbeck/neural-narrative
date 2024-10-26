from pathlib import Path
from typing import Dict

from src.base.constants import TEMPLATE_FILES
from src.base.enums import TemplateType
from src.filesystem.file_operations import read_json_file


class TemplatesRepository:
    @staticmethod
    def load_template(place_type: TemplateType) -> Dict:
        file_path = TEMPLATE_FILES.get(place_type)
        if not file_path:
            raise ValueError(f"Template file for place type '{place_type}' not found.")
        return read_json_file(Path(file_path))
