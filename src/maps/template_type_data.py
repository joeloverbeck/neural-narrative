from dataclasses import dataclass
from pathlib import Path
from typing import Type

from pydantic import BaseModel


@dataclass
class TemplateTypeData:
    prompt_file: Path
    response_model: Type[BaseModel]
