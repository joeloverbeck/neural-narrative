from pydantic import BaseModel, Field


class SpeechTurnChoice(BaseModel):
    identifier: int = (
        Field(
            ...,
            description=(
                "The numeric identifier of the participant who will speak the next line of dialogue in "
                "the ongoing conversation. You must choose only among the allowed participants."
            ),
        ),
    )
    name: str = Field(
        ...,
        description=(
            "The name of the participant who will speak the next line of dialogue."
        ),
    )
    reason: str = Field(
        ...,
        description=(
            "The reason why this participant has been chosen to speak the next line of dialogue."
        ),
    )
