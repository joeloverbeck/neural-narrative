from typing import Type

from pydantic import BaseModel, Field


class Speech(BaseModel):
    chain_of_thought: str = Field(
        ...,
        description="Think step by step to determine the character's speech. It should be relevant to the dialogue, and uniquely fitting to the character.",
    )
    speech: str


def get_custom_speech_turn_class(speaker_name: str) -> Type[BaseModel]:
    class SpeechTurn(BaseModel):
        name: str = Field(
            ...,
            description=(
                f"The name of the character who is speaking. In this case, {speaker_name}. Write ONLY as {speaker_name}, based on the bio above."
            ),
        )
        narration_text: str = Field(
            ...,
            description=(
                f"Narration text describing the character's thoughts and/or actions during {speaker_name}'s speech. Here is an example: {speaker_name} sits up and faces the interlocutor."
            ),
        )
        speech: Speech = Field(
            ...,
            description=(
                f"{speaker_name}'s speech. Base {speaker_name}'s speech pattern on the bio above. Pay attention to the provided speech patterns to mimic them."
            ),
        )

    return SpeechTurn
