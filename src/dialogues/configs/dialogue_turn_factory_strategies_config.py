from dataclasses import dataclass

from src.dialogues.abstracts.strategies import (
    InvolvePlayerInDialogueStrategy,
    DetermineSystemMessageForSpeechTurnStrategy,
)


@dataclass
class DialogueTurnFactoryStrategiesConfig:
    involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategy
    determine_system_message_for_speech_turn_strategy: (
        DetermineSystemMessageForSpeechTurnStrategy
    )
