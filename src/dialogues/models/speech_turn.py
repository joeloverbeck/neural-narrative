from pydantic import BaseModel, Field


class SpeechTurn(BaseModel):
    name: str = Field(
        ...,
        description=(
            "The name of the character who is speaking. In this case, [NAME]. Write ONLY as [NAME], based on the bio above."
        ),
    )
    narration_text: str = Field(
        ...,
        description=(
            "Narration text describing the character's thoughts and/or actions the character's speech. Here is an example: [NAME] sits up and faces the interlocutor."
        ),
    )
    speech: str = Field(
        ...,
        description=(
            "[NAME]'s speech. Base [NAME]'s speech pattern on the bio above. Pay attention to the provided speech patterns to mimic them."
        ),
    )
