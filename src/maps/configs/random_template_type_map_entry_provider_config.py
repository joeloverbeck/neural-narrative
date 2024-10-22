from dataclasses import dataclass
from typing import Optional
from src.base.enums import TemplateType


@dataclass
class RandomTemplateTypeMapEntryProviderConfig:
    father_identifier: Optional[str]
    father_template: str
    place_type: TemplateType
    father_place_type: TemplateType
