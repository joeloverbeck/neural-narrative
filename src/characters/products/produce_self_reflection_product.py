from typing import Optional

from src.base.required_string import RequiredString


class ProduceSelfReflectionProduct:
    def __init__(
        self, self_reflection: RequiredString, voice_line_url: Optional[RequiredString]
    ):
        self._self_reflection = self_reflection
        self._voice_line_url = voice_line_url

    def get_self_reflection(self) -> RequiredString:
        return self._self_reflection

    def get_voice_line_file_name(self) -> RequiredString:
        return self._voice_line_url
