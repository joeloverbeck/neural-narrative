from dataclasses import dataclass
from typing import Optional, Dict

from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


@dataclass
class LlmSpeechDataProviderConfig:
    playthrough_name: str
    speaker_name: str
    participants: Participants
    purpose: Optional[str]
    transcription: Transcription
    summary_notes: Dict[str, Dict[str, str]]
