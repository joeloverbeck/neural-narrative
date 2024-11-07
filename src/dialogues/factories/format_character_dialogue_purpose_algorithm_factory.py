from src.base.validators import validate_non_empty_string
from src.dialogues.algorithms.format_character_dialogue_purpose_algorithm import (
    FormatCharacterDialoguePurposeAlgorithm,
)


class FormatCharacterDialoguePurposeAlgorithmFactory:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def create_algorithm(self, character_identifier: str, character_name: str):
        return FormatCharacterDialoguePurposeAlgorithm(
            self._playthrough_name, character_identifier, character_name
        )
