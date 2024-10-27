from pydantic import BaseModel, Field


class NarrativeBeat(BaseModel):
    narrative_beat: str = Field(
        ...,
        description=(
            "The three or four sentences that naturally progress the actions of the characters, in the present tense, without including any dialogue. Follow the provided instructions."
        ),
    )
