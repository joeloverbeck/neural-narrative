from pydantic import BaseModel, Field


class DialogueSummary(BaseModel):
    summary: str = Field(
        ...,
        description=(
            "The summary of the provided dialogue. To create the summary, follow the instructions. "
            "The summary must be written in the past tense."
        ),
    )
