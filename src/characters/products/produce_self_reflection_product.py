from typing import Optional


class ProduceSelfReflectionProduct:

    def __init__(self, self_reflection: str, voice_line_url: Optional[str]):
        self._self_reflection = self_reflection
        self._voice_line_url = voice_line_url

    def get_self_reflection(self) -> str:
        return self._self_reflection

    def get_voice_line_file_name(self) -> str:
        return self._voice_line_url
