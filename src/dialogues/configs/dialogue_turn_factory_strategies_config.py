from dataclasses import dataclass

from src.dialogues.abstracts.strategies import (
    InvolvePlayerInDialogueStrategy,
)
from src.dialogues.algorithms.determine_next_speaker_algorithm import (
    DetermineNextSpeakerAlgorithm,
)


@dataclass
class DialogueTurnFactoryStrategiesConfig:
    involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategy
    determine_next_speaker_algorithm: DetermineNextSpeakerAlgorithm
