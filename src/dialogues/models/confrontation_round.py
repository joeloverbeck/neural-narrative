from pydantic import BaseModel, Field


class Confrontation(BaseModel):
    chain_of_thought: str = Field(
        ...,
        description=(
            "Think step by step to determine the confrontation round. It should describe brief segment "
            "(approximately ten seconds) of a confrontation within a rich, immersive world. Your narrative should be engaging, "
            "realistic, and reflect the abilities and circumstances of the participants suggested by the user-provided context."
        ),
    )
    narration: str


class ConfrontationRound(BaseModel):
    confrontation_round: Confrontation = Field(
        ...,
        description=(
            "The vivid, dynamic narrative that depicts approximately ten seconds of the confrontation, focusing on the immediate actions and reactions of the characters involved. "
            "Important: do not repeat verbatim previous confrontation rounds: there should always be a progress in the confrontation. Follow the provided instructions."
        ),
    )
