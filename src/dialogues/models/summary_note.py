from typing import Type, Dict

from pydantic import BaseModel, Field


def get_custom_summary_note_class(speaker_name: str) -> Type[BaseModel]:
    class SummaryNote(BaseModel):
        inferences: Dict[str, Dict[str, str]] = Field(
            ...,
            description=(
                f"The inferences that {speaker_name} can make about all the other participants. Follow the provided instructions."
            ),
        )

    return SummaryNote
