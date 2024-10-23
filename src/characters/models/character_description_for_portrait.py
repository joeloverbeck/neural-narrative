from pydantic import BaseModel, Field


class CharacterDescriptionForPortrait(BaseModel):
    description: str = Field(
        ...,
        description=(
            "The detailed and vivid description of the character's appearance, suitable for an image-generating AI. Follow the provided instructions."
        ),
    )
