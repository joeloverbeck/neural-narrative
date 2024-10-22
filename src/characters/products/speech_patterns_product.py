from typing import Optional, List


class SpeechPatternsProduct:

    def __init__(self, speech_patterns: Optional[List[str]], is_valid: bool,
                 error: Optional[str] = None):
        self._speech_patterns = speech_patterns
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[str]:
        return self._speech_patterns

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
