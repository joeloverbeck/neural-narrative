from typing import Optional

from src.dialogues.abstracts.factory_products import PlaceDataForDialoguePromptProduct


class ConcretePlaceDataForDialoguePromptProduct(PlaceDataForDialoguePromptProduct):
    def __init__(self, place_data_for_dialogue: dict, is_valid: bool, error: Optional[str] = None):
        self._place_data_for_dialogue = place_data_for_dialogue
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._place_data_for_dialogue

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
