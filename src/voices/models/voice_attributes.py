from pydantic import BaseModel, Field

from src.voices.enums import (
    VoiceGenderEnum,
    VoiceAgeEnum,
    VoiceEmotionEnum,
    VoiceTempoEnum,
    VoiceVolumeEnum,
    VoiceTextureEnum,
    VoiceToneEnum,
    VoiceStyleEnum,
    VoicePersonalityEnum,
    VoiceSpecialEffectsEnum,
)


class VoiceAttributes(BaseModel):
    voice_gender: VoiceGenderEnum = Field(
        ...,
        description="The fitting gender for the voice this character would have. Choose only among the provided options.",
    )
    voice_age: VoiceAgeEnum = Field(
        ...,
        description="The fitting age for the voice this character would have. Choose only among the provided options.",
    )
    voice_emotion: VoiceEmotionEnum = Field(
        ...,
        description="The fitting main emotion for the voice this character would have. Choose only among the provided options.",
    )
    voice_tempo: VoiceTempoEnum = Field(
        ...,
        description="The fitting tempo for the voice this character would have. Choose only among the provided options.",
    )
    voice_volume: VoiceVolumeEnum = Field(
        ...,
        description="The fitting volume for the voice this character would have. Choose only among the provided options.",
    )
    voice_texture: VoiceTextureEnum = Field(
        ...,
        description="The fitting texture for the voice this character would have. Choose only among the provided options.",
    )
    voice_tone: VoiceToneEnum = Field(
        ...,
        description="The fitting tone for the voice this character would have. Choose only among the provided options.",
    )
    voice_style: VoiceStyleEnum = Field(
        ...,
        description="The fitting style for the voice this character would have. Choose only among the provided options.",
    )
    voice_personality: VoicePersonalityEnum = Field(
        ...,
        description="The fitting personality for the voice this character would have. Choose only among the provided options.",
    )
    voice_special_effects: VoiceSpecialEffectsEnum = Field(
        ...,
        description="The fitting special effects for the voice this character would have. Choose only among the provided options.",
    )

    class Config:
        use_enum_values = True  # Ensures enums are serialized by their values
