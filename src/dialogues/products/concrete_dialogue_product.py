from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription


class ConcreteDialogueProduct(DialogueProduct):

    def __init__(self, messages_to_llm: MessagesToLlm, transcription:
    Transcription, has_ended: bool):
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._has_ended = has_ended

    def get_messages_to_llm(self) -> MessagesToLlm:
        return self._messages_to_llm

    def get_transcription(self) -> Transcription:
        return self._transcription

    def has_ended(self) -> bool:
        return self._has_ended
