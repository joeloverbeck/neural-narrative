from pydantic import BaseModel, Field


class Antagonist(BaseModel):
    antagonist: str = Field(
        ...,
        description=(
            "A complex and intriguing antagonist profile for the story. Follow the provided instructions."
        ),
    )
