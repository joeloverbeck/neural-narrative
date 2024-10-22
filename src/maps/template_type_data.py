from dataclasses import dataclass


@dataclass
class TemplateTypeData:
    prompt_file: str
    father_templates_file_path: str
    current_place_templates_file_path: str
    tool_file: str
