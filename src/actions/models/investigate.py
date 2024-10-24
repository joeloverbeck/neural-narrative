from pydantic import BaseModel, Field


class Investigate(BaseModel):
    narrative: str = Field(
        ...,
        description=(
            "A few descriptive paragraphs detailing a narrative that describes the player's "
            "investigation endeavor within a rich, immersive world."
        ),
    )
    outcome: str = Field(
        ...,
        description="The results of the investigate action based on the assessment.",
    )
