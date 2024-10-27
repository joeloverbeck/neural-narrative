from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy


class EventNarrationForDialogueStrategy(NarrationForDialogueStrategy):

    def __init__(self, event_message: str):
        validate_non_empty_string(event_message, "event_message")

        self._event_message = event_message

    def produce_narration(self) -> str:
        return self._event_message
