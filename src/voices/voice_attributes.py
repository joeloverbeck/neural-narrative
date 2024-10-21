from dataclasses import dataclass
from typing import Optional

from src.base.required_string import RequiredString


@dataclass
class VoiceAttributes:
    voice_gender: Optional[str]
    voice_age: Optional[str]
    voice_emotion: Optional[str]
    voice_tempo: Optional[str]
    voice_volume: Optional[str]
    voice_texture: Optional[str]
    voice_tone: Optional[str]
    voice_style: Optional[str]
    voice_personality: Optional[RequiredString]
    voice_special_effects: Optional[str]
