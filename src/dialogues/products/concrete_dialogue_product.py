from typing import Dict

from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.transcription import Transcription


class ConcreteDialogueProduct(DialogueProduct):

    def __init__(
        self,
        transcription: Transcription,
        summary_notes: Dict[str, Dict[str, Dict[str, str]]],
        has_ended: bool,
    ):
        self._transcription = transcription
        self._summary_notes = summary_notes
        self._has_ended = has_ended

    def get_transcription(self) -> Transcription:
        return self._transcription

    def get_summary_notes(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        return self._summary_notes

    def has_ended(self) -> bool:
        return self._has_ended
