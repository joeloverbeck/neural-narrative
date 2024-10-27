from typing import Type, Optional

from pydantic import BaseModel, Field


class Speech(BaseModel):
    chain_of_thought: str = Field(
        ...,
        description="Think step by step to determine the character's speech. It should be relevant to the dialogue, "
        "and uniquely fitting to the character. Do not repeat previous lines of dialogue unless there's a very good reason.",
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
        narration_text: Optional[str] = Field(
            description=f"Narration text describing the character's thoughts and/or actions during {speaker_name}'s speech. Here is an example: {speaker_name} sits up and faces the interlocutor.",
            default=None,
        )
        speech: Speech = Field(
            ...,
            description=(
                f"{speaker_name}'s speech. Pay attention to {speaker_name}'s speech patterns to determine the character's unique voice. Important: do not repeat {speaker_name}'s previous utterances in the dialogue."
            ),
        )

    return SpeechTurn
