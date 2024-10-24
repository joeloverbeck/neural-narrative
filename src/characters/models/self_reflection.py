from pydantic import BaseModel, Field


class SelfReflection(BaseModel):
    self_reflection: str = Field(
        ...,
        description=(
            "The meaningful and compelling self-reflection in the first-person perspective of the character. Follow the provided instructions."
        ),
    )
