from pydantic import BaseModel, Field, conlist


class BrainstormedEvents(BaseModel):
    events: conlist(str, min_length=5, max_length=5) = Field(
        ...,
        description=(
            "A list of five possible, distinct events that would naturally follow from the ongoing dialogue and context. "
            "Each event should be 1-2 sentences long, written in the present tense."
        ),
    )
