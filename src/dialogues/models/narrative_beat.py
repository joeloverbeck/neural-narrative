from pydantic import BaseModel, Field


class Beat(BaseModel):
    chain_of_thought: str = Field(
        ...,
        description="Think step by step to determine the narrative beat. It should be relevant to the dialogue, "
        "and progress the circumstances in a fitting, meaningful way, following logically.",
    )
    narrative_beat: str


class NarrativeBeat(BaseModel):
    narrative_beat: Beat = Field(
        ...,
        description=(
            "The three or four sentences that naturally progress the actions of the characters, in the present tense, without including any dialogue. Follow the provided instructions."
        ),
    )
