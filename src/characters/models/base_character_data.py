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


class BaseCharacterData(BaseModel):
    name: str = Field(
        ...,
        description=(
            "The name of the character. You are prohibited from using any of the names listed as prohibited in the above instructions."
        ),
    )
    description: str = Field(
        ...,
        description=(
            "Any physical description pieces belong here, as attributes separated by + symbols, e.g. tall + red hair + one-handed sword. "
            "Only include elements that would be visually obvious (e.g. no hidden equipment). Include the character's gender, apparent age, and species."
        ),
    )
    personality: str = Field(
        ...,
        description=(
            "The traits of the character's personality, also broken down into attributes separated by + symbols, e.g. brave + stoic + disillusioned + humble + compassionate + righteous + loyal + inclusive + earnest + straightforward + grounded + protective"
        ),
    )
    profile: str = Field(
        ...,
        description=(
            "The character's bio, following the instructions about the bio requirements."
        ),
    )
    likes: str = Field(
        ...,
        description="The character's likes.",
    )
    dislikes: str = Field(
        ...,
        description="The character's dislikes.",
    )
    secrets: str = Field(
        ...,
        description="The character's secrets. They must be compelling and truly worth being hidden for the character.",
    )
    health: str = Field(
        ...,
        description=(
            "A textual measure of how healthy the character is. Examples: Full health. Another example: Broken arm. "
            "Another example: Chronic pain in knee, and heart issues."
        ),
    )
    equipment: str = Field(
        ...,
        description=(
            "A list of all the equipment that the character has in his or her person. It includes clothing, jewelry, weapons, tools, etc."
        ),
    )
    voice_gender: VoiceGenderEnum = Field(
        ...,
        description="The fitting gender for the voice this character would have. Choose among the provided options.",
    )
    voice_age: VoiceAgeEnum = Field(
        ...,
        description="The fitting age for the voice this character would have. Choose among the provided options.",
    )
    voice_emotion: VoiceEmotionEnum = Field(
        ...,
        description="The fitting main emotion for the voice this character would have. Choose among the provided options.",
    )
    voice_tempo: VoiceTempoEnum = Field(
        ...,
        description="The fitting tempo for the voice this character would have. Choose among the provided options.",
    )
    voice_volume: VoiceVolumeEnum = Field(
        ...,
        description="The fitting volume for the voice this character would have. Choose among the provided options.",
    )
    voice_texture: VoiceTextureEnum = Field(
        ...,
        description="The fitting texture for the voice this character would have. Choose among the provided options.",
    )
    voice_tone: VoiceToneEnum = Field(
        ...,
        description="The fitting tone for the voice this character would have. Choose among the provided options.",
    )
    voice_style: VoiceStyleEnum = Field(
        ...,
        description="The fitting style for the voice this character would have. Choose among the provided options.",
    )
    voice_personality: VoicePersonalityEnum = Field(
        ...,
        description="The fitting personality for the voice this character would have. Choose among the provided options.",
    )
    voice_special_effects: VoiceSpecialEffectsEnum = Field(
        ...,
        description="The fitting special effects for the voice this character would have. Choose among the provided options.",
    )

    class Config:
        use_enum_values = True  # Ensures enums are serialized by their values
