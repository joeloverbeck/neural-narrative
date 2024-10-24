from pydantic import BaseModel, Field


class Research(BaseModel):
    narrative: str = Field(
        ...,
        description=(
            "A few descriptive paragraphs of narrative detailing the player's research endeavor "
            "within a rich, immersive world."
        ),
    )
    outcome: str = Field(
        ...,
        description="The results of the research action based on the assessment.",
    )
