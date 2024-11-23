from typing import Dict

from pydantic import BaseModel, Field


class ReasonedPlaceFacts(BaseModel):
    chain_of_thought: str = Field(
        ...,
        description=(
            "Think step by step to succinctly summarize the facts about the place based on the description above. Make sure to capture all important details."
        ),
    )
    place_facts: Dict[str, str]


class PlaceFacts(BaseModel):
    place_facts: ReasonedPlaceFacts = Field(
        ...,
        description="The facts about the place based on the provided description.",
    )
