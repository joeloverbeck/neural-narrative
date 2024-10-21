from dataclasses import dataclass
from typing import Optional

from src.base.required_string import RequiredString
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


@dataclass
class DialogueTurnFactoryConfig:
    playthrough_name: RequiredString
    participants: Participants
    messages_to_llm: Optional[MessagesToLlm] = None
    transcription: Optional[Transcription] = None
