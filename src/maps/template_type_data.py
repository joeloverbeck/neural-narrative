from dataclasses import dataclass
from typing import Type

from pydantic import BaseModel


@dataclass
class TemplateTypeData:
    prompt_file: str
    father_templates_file_path: str
    current_place_templates_file_path: str
    response_model: Type[BaseModel]
