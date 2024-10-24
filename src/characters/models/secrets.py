from pydantic import BaseModel, Field


class Secrets(BaseModel):
    secrets: str = Field(
        ...,
        description=(
            "The compelling and meaningful secrets, that are truly worth being hidden. Follow the provided instructions."
        ),
    )
