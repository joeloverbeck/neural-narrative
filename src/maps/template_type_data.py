from dataclasses import dataclass

from src.base.required_string import RequiredString


@dataclass
class TemplateTypeData:
    prompt_file: RequiredString
    father_templates_file_path: RequiredString
    current_place_templates_file_path: RequiredString
    tool_file: RequiredString
