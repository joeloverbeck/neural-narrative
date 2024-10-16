from dataclasses import dataclass
from typing import List


@dataclass
class CharacterDataForStorage:
    name: str
    description: str
    personality: str
    profile: str
    likes: str
    dislikes: str
    secrets: str
    speech_patterns: List[str]
    health: str
    equipment: str
    voice_gender: str
    voice_age: str
    voice_emotion: str
    voice_tempo: str
    voice_volume: str
    voice_texture: str
    voice_tone: str
    voice_style: str
    voice_personality: str
    voice_special_effects: str

    def __post_init__(self):
        required_fields = [
            "name",
            "description",
            "personality",
            "profile",
            "likes",
            "dislikes",
            "secrets",
            "speech_patterns",
            "health",
            "equipment",
            "voice_gender",
            "voice_age",
            "voice_emotion",
            "voice_tempo",
            "voice_volume",
            "voice_texture",
            "voice_tone",
            "voice_style",
            "voice_personality",
            "voice_special_effects",
        ]
        for field_name in required_fields:
            value = getattr(self, field_name)
            if not value:
                raise ValueError(
                    f"CharacterData field '{field_name}' is required and cannot be empty."
                )

        if len(self.speech_patterns) != 10:
            raise ValueError(
                "CharacterData field 'speech_patterns' must have exactly 10 items."
            )
