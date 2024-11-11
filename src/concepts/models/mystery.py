from pydantic import BaseModel, Field


class Mystery(BaseModel):
    mystery: str = Field(
        ...,
        description=(
            "A compelling mystery for the player to investigate. Follow the provided instructions."
        ),
    )
