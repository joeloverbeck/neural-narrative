from dataclasses import dataclass

from src.dialogues.abstracts.strategies import (
    InvolvePlayerInDialogueStrategy,
)


@dataclass
class DialogueTurnFactoryStrategiesConfig:
    involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategy
