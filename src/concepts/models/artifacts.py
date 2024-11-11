from pydantic import BaseModel, Field


class Artifacts(BaseModel):
    artifact: str = Field(
        ...,
        description=(
            "A unique artifact or item that the player might encounter. "
            "Follow the provided instructions."
        ),
    )
