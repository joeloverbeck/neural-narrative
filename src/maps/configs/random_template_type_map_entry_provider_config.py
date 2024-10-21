from dataclasses import dataclass
from typing import Optional

from src.base.enums import TemplateType
from src.base.required_string import RequiredString


@dataclass
class RandomTemplateTypeMapEntryProviderConfig:
    father_identifier: Optional[RequiredString]
    father_template: RequiredString
    place_type: TemplateType
    father_place_type: TemplateType
