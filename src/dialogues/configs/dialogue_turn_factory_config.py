from dataclasses import dataclass
from typing import Optional

from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


@dataclass
class DialogueTurnFactoryConfig:
    playthrough_name: str
    player_identifier: str
    participants: Participants
    transcription: Optional[Transcription] = None
