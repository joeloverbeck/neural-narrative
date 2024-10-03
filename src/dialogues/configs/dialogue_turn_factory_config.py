from dataclasses import dataclass
from typing import Optional

from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription


@dataclass
class DialogueTurnFactoryConfig:
    playthrough_name: str
    messages_to_llm: Optional[MessagesToLlm] = None
    transcription: Optional[Transcription] = None
