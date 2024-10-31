from pydantic import BaseModel, Field


class Event(BaseModel):
    chain_of_thought: str = Field(
        ...,
        description=(
            "Think step by step to determine how to develop the user's suggested event into a narrative that "
            "seamlessly integrates into the ongoing story. The narrative should enhance the scene by vividly describing the event, "
            "focusing on the actions, emotions, and reactions of the characters involved. "
            "Important: don't repeat verbatim the event suggestion the user has provided."
        ),
    )
    event: str


class GrowEvent(BaseModel):
    grow_event: Event = Field(
        ...,
        description=(
            "The third-person narrative text of four or five sentences, written in the present tense, that seamlessly integrates into the ongoing story. Follow the provided instructions."
        ),
    )
