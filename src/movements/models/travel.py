from pydantic import BaseModel, Field


class Travel(BaseModel):
    narrative: str = Field(
        ...,
        description=(
            "A compelling narrative in about 10 sentences that captures the essence of the player's journey from the origin area to the destination area."
        ),
    )
    outcome: str = Field(
        ...,
        description="A detailed depiction in about 10 sentences of the outcome of the journey. Follow the instructions in the section 'Outcome - Arrival at Destination'.",
    )
