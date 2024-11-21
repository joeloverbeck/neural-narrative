from dataclasses import dataclass
from typing import Optional, Dict

from src.dialogues.transcription import Transcription


@dataclass
class DialogueTurnFactoryConfig:
    playthrough_name: str
    summary_notes: Dict[str, Dict[str, Dict[str, str]]]
    transcription: Optional[Transcription] = None
