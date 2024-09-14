from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.transcription import Transcription


class ConcreteDialogueProduct(DialogueProduct):
    def get(self) -> Transcription:
        return self._transcription

    def __init__(self, transcription: Transcription):
        # Note that the dialogue may be empty

        self._transcription = transcription
