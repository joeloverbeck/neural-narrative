from dataclasses import dataclass

from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.dialogues.algorithms.format_character_dialogue_purpose_algorithm import (
    FormatCharacterDialoguePurposeAlgorithm,
)


@dataclass
class LlmSpeechDataProviderAlgorithmsConfig:
    format_character_dialogue_purpose_algorithm: FormatCharacterDialoguePurposeAlgorithm
    format_known_facts_algorithm: FormatKnownFactsAlgorithm
