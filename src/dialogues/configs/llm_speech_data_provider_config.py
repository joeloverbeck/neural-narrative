from dataclasses import dataclass
from typing import Optional

from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


@dataclass
class LlmSpeechDataProviderConfig:
    playthrough_name: str
    speaker_identifier: str
    speaker_name: str
    participants: Participants
    purpose: Optional[str]
    transcription: Transcription
