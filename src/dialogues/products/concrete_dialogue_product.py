from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.transcription import Transcription


class ConcreteDialogueProduct(DialogueProduct):

    def __init__(self, transcription: Transcription, has_ended: bool):
        self._transcription = transcription
        self._has_ended = has_ended

    def get_transcription(self) -> Transcription:
        return self._transcription

    def has_ended(self) -> bool:
        return self._has_ended
