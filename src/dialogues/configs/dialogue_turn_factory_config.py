from dataclasses import dataclass
from typing import Optional

from src.dialogues.transcription import Transcription


@dataclass
class DialogueTurnFactoryConfig:
    playthrough_name: str
    transcription: Optional[Transcription] = None
