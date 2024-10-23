from pydantic import BaseModel, Field, conlist


class SpeechPatterns(BaseModel):
    speech_patterns: conlist(str, min_length=10, max_length=10) = Field(
        ...,
        description=(
            "A list of ten quotes in the character's voice. "
            "Focus on creating a compelling, unique narrative voice for the character."
        ),
    )
