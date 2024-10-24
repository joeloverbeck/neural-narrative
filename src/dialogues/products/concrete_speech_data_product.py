from typing import Optional, Dict

from src.dialogues.abstracts.factory_products import SpeechDataProduct


class ConcreteSpeechDataProduct(SpeechDataProduct):

    def __init__(
        self,
        speech_data: Optional[dict[str, str]],
        is_valid: bool,
        error: Optional[str] = None,
    ):
        self._speech_data = speech_data
        self._is_valid = is_valid
        self._error = error

    def get(self) -> Dict[str, str]:
        return self._speech_data

    def set(self, speech_data: Dict[str, str]) -> None:
        self._speech_data = speech_data

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
