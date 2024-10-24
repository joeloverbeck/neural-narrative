from pydantic import BaseModel, Field


class GatherSupplies(BaseModel):
    narrative: str = Field(
        ...,
        description=(
            "A few descriptive paragraphs of narrative detailing the player's endeavor to "
            "gather supplies within a rich, immersive world."
        ),
    )
    outcome: str = Field(
        ...,
        description=(
            "The results of the Gather Supplies action based on the assessment."
        ),
    )
