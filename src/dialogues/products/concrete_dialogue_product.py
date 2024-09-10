from typing import List

from src.dialogues.abstracts.factory_products import DialogueProduct


class ConcreteDialogueProduct(DialogueProduct):
    def get(self) -> List[str]:
        return self._dialogue

    def __init__(self, dialogue: List[str]):
        # Note that the dialogue may be empty

        self._dialogue = dialogue
